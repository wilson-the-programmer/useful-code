import os

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style, merge_styles
from prompt_toolkit.styles.pygments import style_from_pygments_cls

from pygments.lexers import BashLexer
from pygments.styles import get_style_by_name


bash_words = [
    'alias', 'bg', 'break', 'cd', 'chdir', 'command', 'continue',
    'echo', 'eval', 'exec', 'exit', 'export', 'false', 'fg',
    'getopts', 'hash', 'help', 'history', 'jobs', 'kill', 'let',
    'local', 'printf', 'pwd', 'read', 'readonly', 'return', 'set',
    'shift', 'source', 'test', 'times', 'trap', 'true', 'type',
    'ulimit', 'umask', 'unalias', 'unset', 'wait', 'arch', 'ash',
    'awk', 'base64', 'basename', 'bash', 'bc', 'busybox', 'bzcat',
    'bzip2', 'cat', 'chgrp', 'chmod', 'chown', 'cksum', 'clear',
    'cmp', 'cp', 'cut', 'date', 'dd', 'df', 'diff', 'dirname',
    'dos2unix', 'du', 'egrep', 'env', 'expand', 'expr', 'fgrep',
    'find', 'grep', 'gunzip', 'gzip', 'head', 'id', 'killall',
    'ln', 'ls', 'lsof', 'lzcat', 'md5sum', 'mkdir', 'mkfifo', 'mv',
    'nc', 'nl', 'nohup', 'paste', 'patch', 'pkill', 'printenv',
    'readlink', 'realpath', 'rm', 'rmdir', 'sed', 'sh', 'sha1sum',
    'sleep', 'sort', 'split', 'stat', 'stty', 'sync', 'tac', 'tail',
    'tar', 'tee', 'timeout', 'touch', 'tr', 'truncate', 'tty',
    'uname', 'unexpand', 'unix2dos', 'unlink', 'unxz', 'unzip',
    'usleep', 'wc', 'wget', 'xargs', 'xz', 'xzcat', 'yes', 'zcat'
]


one_dark_style = style_from_pygments_cls(
    get_style_by_name("one-dark")
)


completion_style = Style.from_dict({
    'prompt': 'bold #ff8800',
    '': '#cccccc',
    'completion-menu.completion': 'bg:#008888 #ffffff',
    'completion-menu.completion.current': 'bg:#00aaaa #000000',
    'scrollbar.background': 'bg:#88aaaa',
    'scrollbar.button': 'bg:#222222',
})


style = merge_styles([
    one_dark_style,
    completion_style
])


def get_completer():
    current_files = os.listdir('.')

    return WordCompleter(
        bash_words + current_files,
        ignore_case=True
    )


def main():
    print('Bash Shell\n')

    session = PromptSession(
        lexer=PygmentsLexer(BashLexer),
        style=style,
        auto_suggest=AutoSuggestFromHistory()
    )

    while True:
        try:
            cmd = session.prompt(
                [('class:prompt', '\n@ ')],
                completer=get_completer()
            )

            command = cmd.strip()

            if command == 'exit':
                break

            if command == '.clear':
                os.system('clear')
                continue

            os.system(cmd)

        except (KeyboardInterrupt, EOFError):
            print()
            break

        except:
            pass

    print('GoodBye!')


if __name__ == '__main__':
    main()
    
