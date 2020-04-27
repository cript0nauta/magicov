# Magicov

Does anybody bother you about increasing the testing coverage of your Python
project? Are you tired of writing useless tests just to increase that metric?
Then magicov is for you!

This tool will automatically modify your code so you'll get 100% testing
coverage instantly. How? Just remove all uncovered lines of your project!

This approach will make you have less code to maintain, since most of it (at
least if you have low coverage) will be removed.

# Usage

Install the tool with pip:

```
pip install magicov
```

Then run the Python `coverage` tool to fetch the coverage of your project:

```
coverage run '--include=your_project/*' command_to_run_tests.py
```

Make a backup of your code, and run magicov passing it the file with the
coverage data:

```
magicov .coverage
```

You will see a lot of Python files are modified, but your test suite should
pass anyway. And if everything is ok, you will have 100% coverage! You're ready
to push your code to your master branch and make your boss (or testing-obsesive
coworker) satisfied because of a useless metric!

# Videos

My [!!Con West](http://bangbangcon.com/west/) talk explains how to use Magicov and how
it was designed:

<a href="http://www.youtube.com/watch?feature=player_embedded&v=2bnlI3UpH-w" target="_blank"><img src="http://img.youtube.com/vi/2bnlI3UpH-w/0.jpg" alt="" width="240" height="180" border="10" /></a>

https://www.youtube.com/watch?v=2bnlI3UpH-w

# Disclaimer

This is a joke project. It has no practical purpose at all. If you run
this tool, all untested features of your product will be unusable.

This was just my constructive way of saying that testing coverage is not a
useful metric in software projects. At least, not as important as other, more
related to the product ones.

# Credits

Thanks to the [pasta][pasta] maintainers for writing the tool that allowed me
to write magicov, and for the super fast fixing of the strange bugs I reported
to it.

Also, thanks to all the [Faraday Team][faraday] for letting me write the tool and
use it in our product.

[pasta]: https://github.com/google/pasta/
[faraday]: https://github.com/infobyte/faraday/
