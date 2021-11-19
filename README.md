# Paste as Column Package

## Description

Paste clipboard content in block mode at selection start or mouse click position.

Two mode are possible (arguments “mode”):
  - insert : the block of text is inserted
  - overwrite : the block of text will erase any existing character

No key map or mouse map are provided by default, (to avoid conflict with user configuration) so the users need to specify key-binding /mouse-map to use this plugin. A new option “paste in column” is available in the contextual menu (right click).

When using the click position to insert the block, the plugin need to switch to a virtual space mode: by default it support 200 more characters, but this can be change by setting the max_space argument to another value.

## Key-map example

To map keys to call the pase as column , simply add the following to your user .sublime-keymap file:
```json
{
    "keys": ["ctrl+alt+v"],
    "command": "paste_column",
    "args": {"mode": "insert"}
},
{
    "keys": ["ctrl+alt+shift+v"],
    "command": "paste_column",
    "args": {"mode": "overwrite"}
}
```

## Mouse-map example

To map the plugin to a mouse click, edit (or create) the Default.sublime-keymap file in your user directory:

```json
{
    "button": "button2", "modifiers": ["alt"],
    "press_command": "paste_column"
}
```
