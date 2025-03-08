{ pkgs ? import
    (fetchTarball {
      name = "jpetrucciani-2025-03-08";
      url = "https://github.com/jpetrucciani/nix/archive/3b64ee21efc92a849ebb0c74817d4701e9238a3e.tar.gz";
      sha256 = "08j0w9r89dyxsjbr4nfb1j4kq5q79l11wk5x9lr0lil05mzd9fi0";
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
