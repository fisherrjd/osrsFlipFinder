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
  tools = with jacobi; {
    caddy = [
      zaddy
    ];
    cli = [
      jq
      nixpkgs-fmt
    ];
    python = [
      (python310.withPackages (p: with p; [
        requests
        mypy
        fastapi
        uvicorn
        types-requests
      ]))
    ];
    react = [
      nodePackages.create-react-app
      nodejs
      yarn
    ];
  };

  env = jacobi.enviro {
    inherit name tools;
  };
in
env
