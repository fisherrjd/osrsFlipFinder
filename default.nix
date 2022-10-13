{ jacobi ? import
    (
      fetchTarball {
        name = "jpetrucciani-2022-09-26";
        url = "https://github.com/jpetrucciani/nix/archive/26fa1fff87b005c5674d9093dd01db36bc316863.tar.gz";
        sha256 = "13jafqvxn46aazkvwxw74bpaj8nwrqx8is245bzsrwrjhr13zd7m";
      }
    )
    { }
}:
let
  inherit (jacobi.hax) ifIsLinux ifIsDarwin;

  name = "osrsFlipFinder";
  tools = with jacobi; {
    cli = [
      jq
      nixpkgs-fmt
    ];
    python = [
      #      prospector-177
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
