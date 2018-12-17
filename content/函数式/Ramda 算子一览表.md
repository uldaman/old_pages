Title: Ramda 算子一览表
Author: Martin
Date: 2018-12-16 19:00

| list            | function     | object            | relation                | logic         | math     | string   | type   |
| --------------- | ------------ | ----------------- | ----------------------- | ------------- | -------- | -------- | ------ |
| adjust          | __           | assoc             | clamp                   | allPass       | add      | match    | is     |
| all             | addIndex     | assocPath         | countBy                 | and           | dec      | replace  | isNil  |
| any             | always       | clone             | difference              | anyPass       | divide   | split    | propIs |
| aperture        | ap           | dissoc            | differenceWith          | both          | inc      | test     | type   |
| append          | apply        | dissocPath        | eqBy                    | complement    | mathMod  | toLower  |        |
| chain           | applySpec    | eqProps           | equals                  | cond          | mean     | toString |        |
| concat          | applyTo      | evolve            | gt                      | defaultTo     | median   | toUpper  |        |
| contains        | ascend       | forEachObjIndexed | gte                     | either        | modulo   | trim     |        |
| drop            | binary       | has               | identical               | ifElse        | multiply |          |        |
| dropLast        | bind         | hasIn             | innerJoin               | isEmpty       | negate   |          |        |
| dropLastWhile   | call         | hasPath           | intersection            | not           | product  |          |        |
| dropRepeats     | comparator   | invert            | lt                      | or            | subtract |          |        |
| dropRepeatsWith | compose      | invertObj         | lte                     | pathSatisfies | sum      |          |        |
| dropWhile       | composeK     | keys              | max                     | propSatisfies |          |          |        |
| endsWith        | composeP     | keysIn            | maxBy                   | unless        |          |          |        |
| filter          | composeWith  | lens              | min                     | until         |          |          |        |
| find            | construct    | lensIndex         | minBy                   | when          |          |          |        |
| findIndex       | constructN   | lensPath          | pathEq                  |               |          |          |        |
| findLast        | converge     | lensProp          | propEq                  |               |          |          |        |
| findLastIndex   | curry        | mapObjIndexed     | sortBy                  |               |          |          |        |
| flatten         | curryN       | merge             | sortWith                |               |          |          |        |
| forEach         | descend      | mergeDeepLeft     | symmetricDifference     |               |          |          |        |
| fromPairs       | empty        | mergeDeepRight    | symmetricDifferenceWith |               |          |          |        |
| groupBy         | F            | mergeDeepWith     | union                   |               |          |          |        |
| groupWith       | flip         | mergeDeepWithKey  | unionWith               |               |          |          |        |
| head            | identity     | mergeLeft         |                         |               |          |          |        |
| includes        | invoker      | mergeRight        |                         |               |          |          |        |
| indexBy         | juxt         | mergeWith         |                         |               |          |          |        |
| indexOf         | lift         | mergeWithKey      |                         |               |          |          |        |
| init            | liftN        | objOf             |                         |               |          |          |        |
| insert          | memoizeWith  | omit              |                         |               |          |          |        |
| insertAll       | nAry         | over              |                         |               |          |          |        |
| intersperse     | nthArg       | path              |                         |               |          |          |        |
| into            | o            | pathOr            |                         |               |          |          |        |
| join            | of           | pick              |                         |               |          |          |        |
| last            | once         | pickAll           |                         |               |          |          |        |
| lastIndexOf     | otherwise    | pickBy            |                         |               |          |          |        |
| length          | partial      | project           |                         |               |          |          |        |
| map             | partialRight | prop              |                         |               |          |          |        |
| mapAccum        | pipe         | propOr            |                         |               |          |          |        |
| mapAccumRight   | pipeK        | props             |                         |               |          |          |        |
| mergeAll        | pipeP        | set               |                         |               |          |          |        |
| none            | pipeWith     | toPairs           |                         |               |          |          |        |
| nth             | T            | toPairsIn         |                         |               |          |          |        |
| pair            | tap          | values            |                         |               |          |          |        |
| partition       | then         | valuesIn          |                         |               |          |          |        |
| pluck           | thunkify     | view              |                         |               |          |          |        |
| prepend         | tryCatch     | where             |                         |               |          |          |        |
| range           | unapply      | whereEq           |                         |               |          |          |        |
| reduce          | unary        |                   |                         |               |          |          |        |
| reduceBy        | uncurryN     |                   |                         |               |          |          |        |
| reduced         | useWith      |                   |                         |               |          |          |        |
| reduceRight     |              |                   |                         |               |          |          |        |
| reduceWhile     |              |                   |                         |               |          |          |        |
| reject          |              |                   |                         |               |          |          |        |
| remove          |              |                   |                         |               |          |          |        |
| repeat          |              |                   |                         |               |          |          |        |
| reverse         |              |                   |                         |               |          |          |        |
| scan            |              |                   |                         |               |          |          |        |
| sequence        |              |                   |                         |               |          |          |        |
| slice           |              |                   |                         |               |          |          |        |
| sort            |              |                   |                         |               |          |          |        |
| splitAt         |              |                   |                         |               |          |          |        |
| splitEvery      |              |                   |                         |               |          |          |        |
| splitWhen       |              |                   |                         |               |          |          |        |
| startsWith      |              |                   |                         |               |          |          |        |
| tail            |              |                   |                         |               |          |          |        |
| take            |              |                   |                         |               |          |          |        |
| takeLast        |              |                   |                         |               |          |          |        |
| takeLastWhile   |              |                   |                         |               |          |          |        |
| takeWhile       |              |                   |                         |               |          |          |        |
| times           |              |                   |                         |               |          |          |        |
| transduce       |              |                   |                         |               |          |          |        |
| transpose       |              |                   |                         |               |          |          |        |
| traverse        |              |                   |                         |               |          |          |        |
| unfold          |              |                   |                         |               |          |          |        |
| uniq            |              |                   |                         |               |          |          |        |
| uniqBy          |              |                   |                         |               |          |          |        |
| uniqWith        |              |                   |                         |               |          |          |        |
| unnest          |              |                   |                         |               |          |          |        |
| update          |              |                   |                         |               |          |          |        |
| without         |              |                   |                         |               |          |          |        |
| xprod           |              |                   |                         |               |          |          |        |
| zip             |              |                   |                         |               |          |          |        |
| zipObj          |              |                   |                         |               |          |          |        |
| zipWith         |              |                   |                         |               |          |          |        |
