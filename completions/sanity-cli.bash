#!/usr/bin/env bash
# Bash completion for sanity-cli.
#
# Install:
#   source completions/sanity-cli.bash
#
# Or add to /etc/bash_completion.d/ or ~/.bash_completion.
#
# The completion reads plugin slugs from the Python registry at
# tab-completion time.  Comma-separated lists (e.g. --agents ag,cc)
# are supported: after each comma, remaining slugs that aren't already
# selected are offered.

_sanity_cli_completion() {
    local cur prev words cword
    _init_completion || return

    local subcommands=(
        build up down clean stop start restart status list
        plugins proxy ide test shell pull open snapshot check
        sync_config upgrade
    )

    # --- helpers: read slug lists from the Python registry ----------

    _sanity_slugs() {
        # $1 = kind (base-image, agent, desktop, connector, provider)
        python3 -c "
from sanity_gravity.plugins.registry import default_registry
import os
reg = default_registry(os.path.join('$(pwd)', 'plugins'))
kind = '$1'
b = getattr(reg, kind if kind != 'base-image' else 'base_images', {})
print(' '.join(sorted(b.keys())))
" 2>/dev/null
    }

    _sanity_selected_slugs() {
        # Parse comma-separated value at cursor, return already-chosen slugs.
        local val="$1"
        echo "${val}" | tr ',' '\n' | sort -u
    }

    _sanity_complete_comma_list() {
        # $1 = kind, $2 = current input (may contain commas)
        local kind="$1" input="$2"
        local all_slugs selected

        all_slugs=$(_sanity_slugs "$kind")
        if [[ -z "$all_slugs" ]]; then
            COMPREPLY=()
            return
        fi

        # If input contains a comma, figure out what's already selected
        if [[ "$input" == *,* ]]; then
            # Complete the LAST segment after the comma
            local prefix="${input%,*},"
            local last_segment="${input##*,}"
            selected=$(_sanity_selected_slugs "$input")

            local candidates=""
            for s in $all_slugs; do
                if ! echo "$selected" | grep -qx "$s"; then
                    candidates="${candidates:+$candidates }$prefix$s"
                fi
            done
            COMPREPLY=( $(compgen -W "$candidates" -- "$cur") )
        else
            # No comma yet — offer all slugs
            COMPREPLY=( $(compgen -W "$all_slugs" -- "$cur") )
        fi
    }

    # --- main dispatch --------------------------------------------

    # Complete subcommands (position 1)
    if [[ $cword -eq 1 ]]; then
        COMPREPLY=( $(compgen -W "${subcommands[*]}" -- "$cur") )
        return
    fi

    local subcmd="${words[1]}"

    # Complete flags for 'build'
    if [[ "$subcmd" == "build" ]]; then
        case "$prev" in
            --base)
                _sanity_complete_comma_list "base_image" "$cur"
                return ;;
            --agents|-a)
                _sanity_complete_comma_list "agent" "$cur"
                return ;;
            --desktop|-d)
                _sanity_complete_comma_list "desktop" "$cur"
                return ;;
            --connector|-c)
                _sanity_complete_comma_list "connector" "$cur"
                return ;;
            --provider)
                _sanity_complete_comma_list "provider" "$cur"
                return ;;
            --layer)
                COMPREPLY=( $(compgen -W "base desktop agent connector" -- "$cur") )
                return ;;
            --layer-target)
                # Context-dependent; offer intermediates for convenience
                COMPREPLY=()
                return ;;
        esac

        # If current word starts with --, offer build flags
        if [[ "$cur" == -* ]]; then
            COMPREPLY=( $(compgen -W "
                --no-cache --base-image --layer --layer-target
                --list-intermediates --json
                --base --agents --desktop --connector --provider
            " -- "$cur") )
            return
        fi

        # Positional: variant tags — offer all valid tags
        COMPREPLY=( $(compgen -W "$(_sanity_slugs agent | tr ' ' '\n' | head -1) \
            $(python3 -c "
from sanity_gravity.cli.registry import VALID_TAGS
print(' '.join(VALID_TAGS))
" 2>/dev/null)" -- "$cur") )
        return
    fi

    # Complete flags for 'up'
    if [[ "$subcmd" == "up" ]]; then
        case "$prev" in
            --variant|-v)
                COMPREPLY=( $(compgen -W "
                    $(python3 -c "
from sanity_gravity.cli.registry import VALID_TAGS
print(' '.join(VALID_TAGS))
" 2>/dev/null)
                " -- "$cur") )
                return ;;
            --name|-n)
                COMPREPLY=()
                return ;;
            --password)
                COMPREPLY=()
                return ;;
        esac
        if [[ "$cur" == -* ]]; then
            COMPREPLY=( $(compgen -W "
                --variant --ssh-port --kasm-port --vnc-port --novnc-port
                --password --skip-check --workspace --name
                --cpus --memory --image --recreate --pull
            " -- "$cur") )
            return
        fi
    fi

    # Generic: complete --name/-n for lifecycle/status commands
    if [[ "$subcmd" =~ ^(down|clean|stop|start|restart|status|shell|sync_config|upgrade|ide) ]]; then
        case "$prev" in
            --name|-n)
                COMPREPLY=()
                return ;;
        esac
        if [[ "$cur" == -* ]]; then
            COMPREPLY=( $(compgen -W "--name" -- "$cur") )
            return
        fi
    fi

    # plugins list
    if [[ "$subcmd" == "plugins" ]]; then
        COMPREPLY=( $(compgen -W "list" -- "$cur") )
        return
    fi

    # proxy subcommands
    if [[ "$subcmd" == "proxy" ]]; then
        COMPREPLY=( $(compgen -W "setup status remove" -- "$cur") )
        return
    fi

    # ide subcommands
    if [[ "$subcmd" == "ide" ]]; then
        COMPREPLY=( $(compgen -W "update reinstall" -- "$cur") )
        return
    fi
}

complete -F _sanity_cli_completion sanity-cli
complete -F _sanity_cli_completion sanity_gravity
