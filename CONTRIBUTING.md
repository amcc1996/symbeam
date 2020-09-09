## Contributing to SymBeam
:star: :sparkling_heart: It is special to have the contribution of enthusiast coders and students worldwide so, I must deeply thank you for reading this page and looking forward to improving SymBeam and Engineering teaching. :sparkling_heart: :star:

If you have not read it yet, visit the [Code of Conduct](CODE_OF_CONDUCT.md) of SymBeam to act in accordance.

There might be different reasons why you are currently reading this: you just came by and are scrolling through the files in either an entertaining or instructive way, you found a bug in SymBeam and want to see it fixed or you had a great idea for improving SymBeam and want to get your hands dirty and simply do it (or already have!).

Assuming that you are already familiar with git and GitHub, I will walk you through the steps for contributing to this project, assuming that you either already have a good idea in mind or you are just waiting for it to come along.

1. Contributing to SymBeam is based on [Pull Requests](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests). For this, you can create a brand new git branch on your system and develop your original code.

2. SymBeam uses [Black](https://github.com/psf/black) code formatter and [isort](https://github.com/PyCQA/isort) for sorting imports. To the Pull Request to be accepted, the code shall first be compliant with these. Luckily, you do not have to struggle with black and isort, as the command is already included in SymBeam [Makefile](Makefile), so just make sure to run
```
make format
```
before submitting the pull-request. Additionally, SymBeam adheres to several guidelines of [flake8](https://flake8.pycqa.org/en/latest/). To run flake8 against SymBeam, run
```
make lint
```
in SymBeam root directory. This will check if the current code is compliant with black, isort and flake8. If flake8 fails, a list of issues is printed in the terminal. Please, go through these code style issues and fixe them in your code before submitting the Pull Request.

3. Make sure your code did not break anything in earlier releases. For that, you will need [pytest](https://docs.pytest.org/en/stable/contents.html) and [pytest-mpl](https://pypi.org/project/pytest-mpl/) to run
```
make tests
```
and assess if all tests are passed. Also, you are encouraged to include new tests for the novel features introduced by yourself.

4. Submit the Pull Request on GitHub. This will be reviewed and if everything is according to the previous points, your contributions will be merged with the SymBeam master code.

## Support

If you still have any doubt, please contact me:
 * Check the [support](SUPPORT.md)
 * amcc@fe.up.pt
 * antonio.mccarneiro@gmail.com
 
Thank you for your dedication in contribution to develop a healthy and sustainable community,
António Carneiro
