#!/usr/bin/env python3

# std
import os
import pathlib

# ours
from ankipandas.ankipandas import AnkiPandas


# todo: automatically find database
def get_cards_df(
    path,
    deck_names=True,
    merge_notes=True,
    expand_fields=True
):
    """
    Return all cards as a pandas dataframe.

    Args:
        path: Path to database
        merge_notes: Merge information from the notes (default True), e.g. all
            of the fields.
        deck_names: Add a column "deck_names" in addition to the did (deck id)
            column (default True)
        expand_fields:
            When merging notes, epxand the 'flds' column to have a column for
            every field.
    Returns:
        Pandas dataframe
    """
    ap = AnkiPandas(path)
    df = ap.cards(
        deck_names=deck_names,
        merge_notes=merge_notes,
        expand_fields=expand_fields
    )
    del ap
    return df


def _find_anki_path(start_path=None):
    raise NotImplementedError


def _find_users(anki_path: pathlib.Path, user=None,
                collection_filename="collection.anki2"):
    if user:
        potential_users = [user]
    else:
        potential_users = [
            f.name for f in os.scandir(str(anki_path)) if f.is_dir()
        ]
    users = []
    for potential_user in potential_users:
        p = anki_path / potential_user / collection_filename
        if p.is_file():
            users.append(potential_user)
    return users


def find_database(basepath=None, user=None, search_home=True,
                  collection_filename="collection.anki2"):
    """
    
    Args:
        basepath:
        user: 
        search_home: 
        collection_filename: 

    Returns:

    """
    anki_paths = [
        "~/.local/share/Anki2/",
        "~/Documents/Anki2",
        "~/Anki2/"
    ]
    if basepath:
        anki_paths.insert(0, basepath)
    anki_paths = [pathlib.Path(p).expanduser() for p in anki_paths]
    anki_path = None
    for path in anki_paths:
        if not path.is_dir():
            continue
        anki_path = path
        break
    else:
        # Not found
        if search_home:
            anki_path = _find_anki_path()
    if not anki_path:
        raise RuntimeError("Could not find database.")

    if user:
        users = [user]
    else:
        users = _find_users(anki_path, collection_filename=collection_filename)
    if len(users) == 0:
        raise RuntimeError(
            "No database found in anki directory {}".format(anki_path)
        )
    if len(users) >= 2:
        raise RuntimeError(
            "More than one user account found in anki directory {}: {} "
            "Please select one with the 'user' keyword.".format(
                anki_path,
                ", ".join(users)
            )
        )

    # Everything good
    return anki_path / users[0] / collection_filename
