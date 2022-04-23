"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

Copied from https://github.com/tgstation/gbp-action/blob/eeead96cb1f16f23dbe103274b652aedbef017f1/src/configuration.ts with modifications.
"""

import { promises as fs } from "fs"
import { isRight } from "fp-ts/lib/Either"
import * as t from "io-ts"
import * as toml from "toml"
import path from "path"

export type Configuration = {
    collection_method?: "high_vs_low" | "sum"
    maintainer_team_slug?: string
    no_balance_label?: string
    reset_label?: string

    points: Map<string, number>
}

const configurationSchema = t.intersection([
    t.partial({
        collection_method: t.union([
            // Adds the top scoring positive label to the lowest scoring negative label (default)
            t.literal("high_vs_low"),

            // Adds all point labels together
            t.literal("sum"),
        ]),
        no_balance_label: t.string,
        reset_label: t.string,
    }),

    t.interface({
        points: t.record(t.string, t.number),
    }),
])

export function parseConfig(configurationText: string): Configuration {
    const valueEither = configurationSchema.decode(
        toml.parse(configurationText),
    )

    if (isRight(valueEither)) {
        const value = valueEither.right

        return {
            ...value,
            points: new Map(Object.entries(value.points)),
        }
    } else {
        throw valueEither.left
    }
}
