import shutil
import os
from dependency import Dependency
from usecases.build_usecase import BuildUsecase

# DI: https://github.com/python-injector/injector


def main(usecase: BuildUsecase) -> None:
    # Remove the 'dist' folder
    shutil.rmtree('dist', ignore_errors=True)

    # Execute the process
    usecase.build()


if __name__ == '__main__':
    # Move the current directory to the parent folder of the directory where this file exists
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Create DI
    injector = Dependency()
    usecase: BuildUsecase = injector.resolve(BuildUsecase)

    main(usecase)
