## Contributing to SymBeam
:star: :sparkling_heart: It is special to have the contribution of enthusiast coders and students worldwide so, I must deeply thank young for reading this page and working for improving SymBeam and Engineering teaching. :sparkling_heart: :star:

If you have not read it yet, visit the [Code of Conduct](CODE_OF_CONDUCT.md) of SymBeam to act in conformity to it.

There are different reasons why you are currently reading this page: you just came by and are scrolling through the files in an either entertaining or instructive way, you found a bug in SymBeam and want to see it fixed or you had a great idea for an improvement of SymBeam and want to put your hands on and do it (or already have!).

Not knowing if you are new to git and GitHub or not, I will walk you through the steps for contributing to this project, assuming that you either already have a good idea in mind or you are just waiting for it to come along.

1. Contributing to SymBeam is based on [Pull Requests](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests). For this, you can create a brand new git branch on your system and develop your original code.

2. SymBeam uses [Black](https://github.com/psf/black) code formatter. In order to the Pull Request to be accepted, the code shall first go through it. You do not struggle with black, as the command is already included in SymBeam [Makefile](Makefile), so just make sure to run
```
make format
```
before submitting the pull-request.

3. Make sure your code did not break anything in earlier releases. For that, you will need [pytest](https://docs.pytest.org/en/stable/contents.html) to run
```
make coverage
```
and assess if all tests are passed. Also, you are advised to include new tests for the novel features introduced by yourself.

4. Submit the Pull Request on GitHub, which will be review and if everything is clean, your contributions will be merged with the SymBeam master code.

If you still have any doubt, please contact me:
 * Check the [support](SUPPORT.md)
 * amcc@fe.up.pt
 * antonio.mccarneiro@gmail.com
 
Thank you for you dedication in contribution to develop a healthy and sustainable community,
António Carneiro
