: ${bats_base_dir:=$(readlink $(dirname $BASH_SOURCE))}

export PATH="$bats_base_dir/bin:$PATH"
export MANPATH="$bats_base_dir/man:$MANPATH"

echo "Added $bats_base_dir/bin to PATH"
