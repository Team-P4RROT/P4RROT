set -e

source config.sh

sudo $P4APP_PATH build .

echo
echo " BMV2 BUILD SUCCEDED "
echo

export P4C_BIN_DIR=$P4C_BIN_DIR

# workaround for missing include
mkdir out
cp /opt/netronome/p4/components/flowcache/me/lib/flowcache/*.h out

# workaround for hdr placement (create dummy parser)
python3 gen_dummy.py > dummy.p4

test -e hook_pre_nfp_build.sh && bash hook_pre_nfp_build.sh

$NFP4BUILD_PATH -p out/ -o simple_router.nffw -l $NFPTARGET -4 main.p4 --nfp4c_p4_version 16 --nfp4c_D TARGET_NFP --nfp4c_D USE_DUMMY_PARSER --disable-component flowcache -D PIF_PLUGIN_INIT -c fsatomic.c /opt/netronome/components/standardlibrary/microc/src/nfp_mem_lockq.c -I /opt/netronome/components/standardlibrary/microc/include/nfp_mem_lockq.h


echo
echo " NFP BUILD SUCCEDED "
echo