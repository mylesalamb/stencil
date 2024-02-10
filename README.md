# Stencil

Stencil is a simple static site generator written in python
that aims to provide simple abstractions to make building websites easier

Where other static site generators bludgeon their users into developing blog-like websites, stencil gives users complete control of what build artefacts are produced and how they are produced.


# Configuration

Stencil is configured through a JSON config either passed as an argument to `stencil build project` with `-c` or through being read through stdin with `-c -`.

An example stencil config looks like...

```
{
    "content": [
        {
            "builder": "static",
            "source_directory": "./root-static",
            "output_directory": ""
        },
        {
            "builder": "template",
            "source_directory": "./root-pages",
            "output_directory": ""
        }
    ],
    "builders": {
        "static": {
            "flavor": "StaticBuilder",
            "config": {
                "symlink": true
            }
        },
        "template": {
            "flavor": "MarkdownBuilder",
            "config": {
                "template_directory": "./templates",
                "markdown_extensions": ["fenced_code"]
            }
        }
    },
    "variables": {
        "site_name": "mylesalamb.com"
    }
}
```

### Content Entries

Content blocks describe where source artefacts live, relative to the current working directory, and where their outputs should be placed relative to the output directory argument.

Each stencil content block is associated with a named 'builder' which provides a build strategy for processing inputs to their associated ouptuts

### Builder Entries

Builders provide a strategy/method for taking an input directory, performing some operation and placing the result in an output directory.

## Building

The project ships with a makefile that makes developing against stencil easy. you can produce a
development build of stencil with `make dev`, you can then run stencil with `./venv/bin/stencil`

## Installing

stencil can be installed through either a `whl` or through using the makefile to install to `/opt`

To build the project as a python wheel

```shell
make dev
make dist
```

Where the wheel is located in `./dist`

To install to `/opt` you can run

```shell
make dev
make dist
sudo make install
```

Where you should then adjust your PATH like so `export PATH=${PATH}:/opt/stencil/bin`

## Bumping dependencies

stencil is built against a contraints file that restricts the versions of dependencies that are installed with stencil, you can bump the dependencies in use with

```shell
make clean
> constraints.txt
make dev
./venv/bin/pip freeze --exclude-editable > constraints.txt
```