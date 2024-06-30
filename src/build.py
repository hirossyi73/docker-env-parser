import shutil
import os

from models.config import GlobalConfig
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from usecases.build_usecase import BuildUsecase

# DI: https://github.com/ets-labs/python-dependency-injector

global_config = GlobalConfig()
global_config.init_config(None, None)


class Container(containers.DeclarativeContainer):
    build_usecase = providers.Singleton(
        BuildUsecase,
        config=global_config,
    )


@inject
def main(usecase: BuildUsecase = Provide[Container.build_usecase]) -> None:
    # distフォルダを削除
    shutil.rmtree('dist', ignore_errors=True)

    # 処理実行
    usecase.build()


if __name__ == '__main__':
    # このファイルがあるディレクトリの一つ上のフォルダに、にカレントディレクトリを移動
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    container = Container()
    container.wire(modules=[__name__])

    main()
