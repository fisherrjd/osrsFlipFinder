{ jacobi ? import
    (
      fetchTarball {
        name = "jpetrucciani-2022-10-12";
        url = "https://github.com/jpetrucciani/nix/archive/d1c781aada62bdbd91fcad427759167ef1c9b59b.tar.gz";
        sha256 = "0j3sy7qpxyaqmqqb0iywlw0ism5qwy2bf73l125rlv9vxxrbjdag";
      }
    )
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
          ${python}/bin/uvicorn main:app --reload
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
      react = [
        nodePackages.create-react-app
        nodejs
        yarn
      ];
      scripts = [
        run-backend
        run-caddy
        run-frontend
        run
      ];
    };

  env = jacobi.enviro {
    inherit name tools;
  };
in
env
