{ pkgs ? import
    (fetchTarball {
      name = "jpetrucciani-2025-05-19";
      url = "https://github.com/jpetrucciani/nix/archive/8dedb8b3f777faba7eab070b443535f12f9a70f7.tar.gz";
      sha256 = "17sn5cy76ix8zi8fni4lavb0ns2s69aqrsic5mq6qh8b56c04pn0";
    })
    { }
}:
let
  name = "osrsFlipFinder";

  uvEnv = pkgs.uv-nix.mkEnv {
    inherit name; python = pkgs.python313;
    workspaceRoot = ./.;
    pyprojectOverrides = final: prev: { };
  };

  tools = with pkgs; {
    cli = [
      jfmt
      nixup
    ];
    uv = [ uv uvEnv ];
    scripts = pkgs.lib.attrsets.attrValues scripts;
  };


  scripts = with pkgs; {
    # Run the backend data collection
    run-data = pkgs.pog {
      name = "run-data";
      script = ''
        cd ./bot/data_collection || exit
        ${uvEnv}/bin/python osrs_to_db.py
      '';
    };
    # Start the discord bot "frontend"
    run-bot = pkgs.pog {
      name = "run-bot";
      script = ''
        cd ./bot || exit
        ${uvEnv}/bin/python bot.py
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
  NIXUP = "0.0.9";
} // uvEnv.uvEnvVars)) // { inherit scripts; }
