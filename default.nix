{ pkgs ? import
    (fetchTarball {
      name = "jpetrucciani-2024-11-20";
      url = "https://github.com/jpetrucciani/nix/archive/b4ecbf87a1a468ce43256b330d0627e7c13d0b7c.tar.gz";
      sha256 = "0flajq0ri2sd9a8901wl48zxnlsjgqy25c0bglhwmlyj1d0gim6v";
    })
    { }
}:
let
  name = "osrsFlipFinder";


  tools = with pkgs; {
    cli = [
      coreutils
      nixpkgs-fmt
      sqlite3
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
        types-requests
        osrsreboxed
        discordpy
        python-dotenv
        sqlite3
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
