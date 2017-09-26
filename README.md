# hymo
hymo: A Hydro Model reader.
`hymo` merges `swmmreport` and `lspcreport` to `hymo`.

The `BaseReader` class of swmmreport is an extensible framework to
several different model input and output files. Previously, `swmmreport` was
a dependency of `lspcreport`. Moving forward new models can easily be added
to this framework without needing `swmmreport.BaseReader()` as a dependency.

`swmmreport` was previously at (https://github.com/lucashtnguyen/swmmreport)
`lspcreport` was previously at (https://github.com/lucashtnguyen/lspcreport)

[![Build Status](https://travis-ci.org/lucashtnguyen/hymo.svg?branch=master)](https://travis-ci.org/lucashtnguyen/hymo)
[![Coverage Status](https://coveralls.io/repos/lucashtnguyen/hymo/badge.svg?branch=master)](https://coveralls.io/r/lucashtnguyen/hymo?branch=master)