{ jacobi ? import
    (fetchTarball {
      name = "jpetrucciani-2023-05-06";
      url = "https://nix.cobi.dev/x/835e1f9c781be24823d4717e201a75db40f1ed2a";
      sha256 = "1zdnvac1r77im43jrkv6jpdzir17dxd82lbwal8jjiz7cvvvis0p";
    })
    { }
}:
let
  name = "osrsFlipFinder";
  tools = with jacobi;
    let
      python = python311.withPackages (p: with p; [
        requests
        pandas
        mypy
        fastapi
        uvicorn
        types-requests
        osrsreboxed
        seaborn
      ]);
      run-caddy = pog {
        name = "run-caddy";
        script = ''
          ${zaddy}/bin/caddy run --config ./conf/Caddyfile --watch "$@"
        '';
      };
      run-frontend = pog {
        name = "run-frontend";
        script = ''
          cd ./flipfinder/ || exit
          BROWSER=none ${nodejs}/bin/npm start
        '';
      };
      run-backend = pog {
        name = "run-backend";
        script = ''
          cd ./flipfinder/src/python/ || exit
          ${python}/bin/uvicorn main:APP --reload
        '';
      };
      run = pog {
        name = "run";
        script = ''
          ${concurrently}/bin/concurrently \
            --names "caddy,react,fastapi" \
            --prefix-colors "cyan,blue,green" \
            "run-caddy" \
            "run-frontend" \
            "run-backend"
        '';
      };
    in
    {
      cli = [
        jq
        nixpkgs-fmt
      ];
      python = [
        python
      ];
      node = [
        (with nodePackages; [
          create-react-app
          prettier
        ])
        nodejs
        yarn
      ];
      scripts = [
        run-backend
        run-caddy
        run-frontend
        run
        (writeShellScriptBin "format" ''
          ${concurrently}/bin/concurrently \
            --names "prettier,black" \
            --prefix-colors "cyan,blue" \
            "${nodePackages.prettier}/bin/prettier --config ${./.prettierrc.js} --write ." \
            "${python310Packages.black}/bin/black ."
        '')
        (writeShellScriptBin "prospector" ''
          ${prospector}/bin/prospector $@
        '')
      ];
    };

  env = jacobi.enviro {
    inherit name tools;
  };
in
env
