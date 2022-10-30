{ jacobi ? import
    (fetchTarball {
      name = "jpetrucciani-2022-10-30";
      url = "https://nix.cobi.dev/x/4ce097d2d2d81bcae41fefe950df97471aacdab3";
      sha256 = "1whplss9y5xbwyi9ac2dyn4iwvxdjm0abv5g5l26h6j3pyb59s73";
    })
    { }
}:
let
  name = "osrsFlipFinder";
  tools = with jacobi;
    let
      python = python310.withPackages (p: with p; [
        requests
        mypy
        fastapi
        uvicorn
        types-requests
        osrsreboxed
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
        (writeShellScriptBin "fmt" ''
          ${concurrently}/bin/concurrently \
            --names "prettier,black" \
            --prefix-colors "cyan,blue" \
            "${nodePackages.prettier}/bin/prettier --config ${./.prettierrc.js} --write ." \
            "${python310Packages.black}/bin/black ."
        '')
      ];
    };

  env = jacobi.enviro {
    inherit name tools;
  };
in
env
