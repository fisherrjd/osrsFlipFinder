{ jacobi ? import
    (
      fetchTarball {
        name = "jpetrucciani-2022-10-13";
        url = "https://github.com/jpetrucciani/nix/archive/0b5f2fa50b8a90499f406033a2581029d8e9221e.tar.gz";
        sha256 = "027kd57k3xzh62f393k81kv1a9wnx0s2bcnw13jnxdzdw9d8pig8";
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
