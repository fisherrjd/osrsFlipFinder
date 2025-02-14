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

  tools = with pkgs;
    {
      cli = [
        jfmt
        nixup
      ];
      python = [
        ruff
        uv
      ];
      scripts = pkgs.lib.attrsets.attrValues scripts;
    };

  scripts = with pkgs; {
    # Run the backend data collection
    run-data = pkgs.pog {
      name = "run-data";
      script = ''
        cd ./bot/data_collection || exit
        uv run python osrs_to_db.py
      '';
    };
    # Start the discord bot "frontend"
    run-bot = pkgs.pog {
      name = "run-bot";
      script = ''
        cd ./bot || exit
        uv run python main.py
      '';
    };

    # Run the "frontend" and the data collection tool
    run = pkgs.pog {
      name = "run";
      script = ''
        ${pkgs.concurrently}/bin/concurrently \
          --names "data_collection,bot" \
          --prefix-colors "cyan,blue,green" \
          "run-data" \
          "run-bot" \
      '';
    };
  };
  paths = pkgs.lib.flatten [ (builtins.attrValues tools) ];
  env = pkgs.buildEnv {
    inherit name paths; buildInputs = paths;
  };
in
(env.overrideAttrs (_: {
  inherit name;
  NIXUP = "0.0.8";
})) // { inherit scripts; }
