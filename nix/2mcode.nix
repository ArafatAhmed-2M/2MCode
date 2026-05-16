{
  lib,
  stdenvNoCC,
  callPackage,
  bun,
  nodejs,
  sysctl,
  makeBinaryWrapper,
  models-dev,
  ripgrep,
  installShellFiles,
  versionCheckHook,
  writableTmpDirAsHomeHook,
  node_modules ? callPackage ./node-modules.nix { },
}:
stdenvNoCC.mkDerivation (finalAttrs: {
  pname = "2M_CODE";
  inherit (node_modules) version src;
  inherit node_modules;

  nativeBuildInputs = [
    bun
    nodejs # for patchShebangs node_modules
    installShellFiles
    makeBinaryWrapper
    models-dev
    writableTmpDirAsHomeHook
  ];

  configurePhase = ''
    runHook preConfigure

    cp -R ${finalAttrs.node_modules}/. .
    patchShebangs node_modules
    patchShebangs packages/*/node_modules

    runHook postConfigure
  '';

  env.MODELS_DEV_API_JSON = "${models-dev}/dist/_api.json";
  env.2M_CODE_DISABLE_MODELS_FETCH = true;
  env.2M_CODE_VERSION = finalAttrs.version;
  env.2M_CODE_CHANNEL = "local";

  buildPhase = ''
    runHook preBuild

    cd ./packages/2M_CODE
    bun --bun ./script/build.ts --single --skip-install
    bun --bun ./script/schema.ts schema.json

    runHook postBuild
  '';

  installPhase = ''
    runHook preInstall

    install -Dm755 dist/2M_CODE-*/bin/2M_CODE $out/bin/2M_CODE
    install -Dm644 schema.json $out/share/2M_CODE/schema.json

    wrapProgram $out/bin/2M_CODE \
      --prefix PATH : ${
        lib.makeBinPath (
          [
            ripgrep
          ]
          # bun runs sysctl to detect if running on rosetta2
          ++ lib.optional stdenvNoCC.hostPlatform.isDarwin sysctl
        )
      }

    runHook postInstall
  '';

  postInstall = lib.optionalString (stdenvNoCC.buildPlatform.canExecute stdenvNoCC.hostPlatform) ''
    # trick yargs into also generating zsh completions
    installShellCompletion --cmd 2M_CODE \
      --bash <($out/bin/2M_CODE completion) \
      --zsh <(SHELL=/bin/zsh $out/bin/2M_CODE completion)
  '';

  nativeInstallCheckInputs = [
    versionCheckHook
    writableTmpDirAsHomeHook
  ];
  doInstallCheck = true;
  versionCheckKeepEnvironment = [ "HOME" "2M_CODE_DISABLE_MODELS_FETCH" ];
  versionCheckProgramArg = "--version";

  passthru = {
    jsonschema = "${placeholder "out"}/share/2M_CODE/schema.json";
  };

  meta = {
    description = "The open source coding agent";
    homepage = "https://2M_CODE.ai/";
    license = lib.licenses.mit;
    mainProgram = "2M_CODE";
    inherit (node_modules.meta) platforms;
  };
})
