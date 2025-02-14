{ pkgs ? import
    (fetchTarball {
      name = "jpetrucciani-2025-02-14";
      url = "https://github.com/jpetrucciani/nix/archive/987b16e4a665dbb0a72b5223de725c2592c9e6ad.tar.gz";
      sha256 = "1f0lsg0w6v4bln295mi9z11gg94rcsqkl7hgph6clg4vkjl0nw6x";
    })
    { }
}:
let
  name = "osrsFlipFinder";


  tools = with pkgs; {
    cli = [
      coreutils
      nixpkgs-fmt
    ];
    python = [
      (python312.withPackages (p: with p; [
        black
        ruff
        requests
        pandas
        mypy
        fastapi
        uvicorn
        fuzzywuzzy
        types-requests
        osrsreboxed
        discordpy
        python-dotenv
        sqlite
        texttable
        tabulate
      ]))
    ];
    scripts = pkgs.lib.attrsets.attrValues scripts;
  };

  scripts = with pkgs; { };
  paths = pkgs.lib.flatten [ (builtins.attrValues tools) ];
  env = pkgs.buildEnv {
    inherit name paths; buildInputs = paths;
  };
in
(env.overrideAttrs (_: {
  inherit name;
  NIXUP = "0.0.8";
})) // { inherit scripts; }


### Script info stuff ###
# run-data = pkgs.pog {
#   name = "run-data";
#   script = ''
#     cd ./flipfinder/bot/data_collection || exit
#     ${tools.python}/bin/python osrs_to_db.py
#   '';
# };

# run-bot = pkgs.pog {
#   name = "run-bot";
#   script = ''
#     cd ./flipfinder/bot || exit
#     ${tools.python}/bin/python main.py
#   '';
# };
# run = pkgs.pog {
#   name = "run";
#   script = ''
#     ${pkgs.concurrently}/bin/concurrently \
#       --names "caddy,react,fastapi" \
#       --prefix-colors "cyan,blue,green" \
#       "run-data" \
#       "run-bot" \
#   '';
# };

# scripts = [
#   run-data
#   run-bot
#   run
# ];
