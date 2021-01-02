# pyOCD debugger
# Copyright (c) 2019-2020 Arm Limited
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ...coresight.coresight_target import CoreSightTarget
from ...core.memory_map import (FlashRegion, RamRegion, MemoryMap)
from ...debug.svd.loader import SVDFile


class DBGMCU:
    STCTL = 0xE0042020
    STCTL_VALUE = 0x7FFFFF

    STCTL1 = 0xE0042028
    STCTL1_VALUE = 0xFFF

    TRACECTL = 0xE0042024
    TRACECTL_VALUE = 0x0

FLASH_ALGO = { 'load_address' : 0x20000000,
               'instructions' : [
    0xE00ABE00, 0x062D780D, 0x24084068, 0xD3000040, 0x1E644058, 0x1C49D1FA, 0x2A001E52, 0x4770D1F2,
    0x4770ba40, 0x4770bac0, 0x0030ea4f, 0x00004770, 0x49052000, 0x49057008, 0x20016008, 0x39264902,
    0x002af881, 0x00004770, 0x40054026, 0x40010418, 0x4004f240, 0xf0006800, 0xb1180001, 0x490b480a,
    0xe0026008, 0x4909480a, 0x20056008, 0x60084909, 0x490a4809, 0x20006208, 0x312a4908, 0x20057008,
    0xf8814906, 0x47700026, 0x22205981, 0x40054100, 0x22204781, 0x40010418, 0x00116310, 0x40054000,
    0x2400b530, 0xf9a6f000, 0x7083f44f, 0x6008491a, 0x4510f44f, 0x60282000, 0x1c64e007, 0x42844817,
    0xf000d303, 0x2001f997, 0x4813bd30, 0x68001d00, 0x7080f400, 0x7f80f5b0, 0x480fd007, 0x68001d00,
    0x7080f000, 0x7f80f1b0, 0xe007d1e7, 0x3008480a, 0xf0406800, 0x49081010, 0x60083108, 0x1d004806,
    0xf0006800, 0x28001010, 0x4903d1f0, 0xf0006008, 0x2000f971, 0x0000e7d8, 0x4001041c, 0x77359400,
    0x4604b530, 0xf0002500, 0x2004f965, 0x60084919, 0x60202000, 0x1c6de007, 0x42854817, 0xf000d303,
    0x2001f959, 0x4813bd30, 0x68001d00, 0x7080f400, 0x7f80f5b0, 0x480fd007, 0x68001d00, 0x7080f000,
    0x7f80f1b0, 0xe007d1e7, 0x3008480a, 0xf0406800, 0x49081010, 0x60083108, 0x1d004806, 0xf0006800,
    0x28001010, 0x4903d1f0, 0xf0006008, 0x2000f933, 0x0000e7d8, 0x4001041c, 0x77359400, 0x4604b570,
    0x4616460d, 0xf926f000, 0x1023f240, 0x60084917, 0x2010f243, 0xf04f6008, 0x491530ff, 0x1d096008,
    0x1d096008, 0x1d096008, 0x1d096008, 0x1d096008, 0x1d096008, 0x1d096008, 0x480e6008, 0x1d09490b,
    0x43c06008, 0x480c6008, 0x31184908, 0x12c06008, 0x60081d09, 0x5001f24a, 0x80084908, 0xff18f7ff,
    0xff26f7ff, 0xf8f6f000, 0xbd702000, 0x40010400, 0x40010590, 0x01234567, 0x00080005, 0x400543fe,
    0x41f8e92d, 0x460c4606, 0x48484617, 0x46b89000, 0x1003f240, 0x60084946, 0x48444635, 0xbf009000,
    0xf8d8f000, 0x0000f8d8, 0xf5b56028, 0xd22b1f80, 0x68004840, 0x42884940, 0x2000d026, 0xe00b9000,
    0x1c409800, 0x49399000, 0x42889800, 0xf000d304, 0x2001f8c1, 0x81f8e8bd, 0x1d004835, 0xf0006800,
    0x28100010, 0xe007d1ec, 0x30084831, 0xf0406800, 0x492f0010, 0x60083108, 0x1d00482d, 0xf0006800,
    0x28100010, 0xe026d0f0, 0x90002000, 0x9800e00a, 0x90001c40, 0x98004925, 0xd3034288, 0xf89af000,
    0xe7d72001, 0x1d004822, 0xf4006800, 0xf5b01080, 0xd1ec1f80, 0x481ee007, 0x68003008, 0x1080f440,
    0x3108491b, 0x481a6008, 0x68001d00, 0x1080f400, 0x1f80f5b0, 0xf108d0ef, 0x1d2d0804, 0x2c041f24,
    0x2000d29e, 0x60084912, 0xe00a9000, 0x1c409800, 0x490e9000, 0x42889800, 0xf000d303, 0x2001f86b,
    0x480be7a8, 0x68001d00, 0x7080f400, 0x7f80f5b0, 0x4807d007, 0x68001d00, 0x7080f000, 0x7f80f1b0,
    0xf000d1e4, 0x2000f857, 0x0000e794, 0x0bebc200, 0x4001041c, 0x03002000, 0x005a5a5a, 0x49034802,
    0x48036008, 0x47706008, 0xffff0123, 0x40049408, 0xffff3210, 0x20004601, 0x60104a03, 0x4a021e40,
    0x60103a1c, 0x47702000, 0x4001041c, 0x4604b5f0, 0x2300460d, 0x27002600, 0x21004626, 0xf856e007,
    0x6810cb04, 0xd0004584, 0x1d12e004, 0xebb11c49, 0xd3f40f95, 0x4637bf00, 0xe0062300, 0xcb01f817,
    0x45845cd0, 0xe004d000, 0xf0051c5b, 0x42980003, 0xbf00d8f4, 0x0081eb04, 0xbdf04418, 0x49034802,
    0x48036088, 0x47706088, 0xffff0123, 0x40049000, 0xffff3210, 0xf44fb500, 0x68006080, 0x3080f400,
    0xf000b908, 0xf44ff855, 0x68006080, 0x0001f000, 0xf000b908, 0xbd00f801, 0x4824b510, 0xb2826800,
    0x6080f44f, 0xf3c06800, 0xf44f0481, 0x68006080, 0x2303f3c0, 0x1192b90c, 0x2c01e008, 0x1292d101,
    0x2c02e004, 0x1312d101, 0x1392e000, 0x2001b90b, 0x2000e000, 0xd1012b0f, 0xe0002101, 0x43082100,
    0xf7ffb110, 0xe020ff7b, 0x0001f003, 0xb9e2b118, 0xff74f7ff, 0xf003e019, 0x28020002, 0x2a01d104,
    0xf7ffd113, 0xe010ff6b, 0x0004f003, 0xd1042804, 0xd10a2a02, 0xff62f7ff, 0xf003e007, 0x28080008,
    0x2a03d103, 0xf7ffd101, 0xbd10ff59, 0x40049404, 0x4824b510, 0xb2826840, 0x6080f44f, 0xf3c06800,
    0xf44f4481, 0x68006080, 0x6303f3c0, 0x1192b90c, 0x2c01e008, 0x1292d101, 0x2c02e004, 0x1312d101,
    0x1392e000, 0x2001b90b, 0x2000e000, 0xd1012b0f, 0xe0002101, 0x43082100, 0xf7ffb110, 0xe020ff6f,
    0x0001f003, 0xb9e2b118, 0xff68f7ff, 0xf003e019, 0x28020002, 0x2a01d104, 0xf7ffd113, 0xe010ff5f,
    0x0004f003, 0xd1042804, 0xd10a2a02, 0xff56f7ff, 0xf003e007, 0x28080008, 0x2a03d103, 0xf7ffd101,
    0xbd10ff4d, 0x40049000, 0x00000000
    ],

    # Relative function addresses
    'pc_init': 0x2000019d,
    'pc_unInit': 0x20000375,
    'pc_program_page': 0x20000221,
    'pc_erase_sector': 0x20000121,
    'pc_eraseAll': 0x200000a1,

    'static_base' : 0x20000000 + 0x00000020 + 0x00000528,
    'begin_stack' : 0x20000800,
    'begin_data' : 0x20000000 + 0x1000,
    'page_size' : 0x800,
    'analyzer_supported' : False,
    'analyzer_address' : 0x00000000,
    'page_buffers' : [0x20001000, 0x20001800],   # Enable double buffering
    'min_program_length' : 0x800,

    # Flash information
    'flash_start': 0x0,
    'flash_size': 0x200000,
    'sector_sizes': (
        (0x0, 0x2000),
    )
}


FLASH_ALGO_OTP = {
    'load_address' : 0x20000000,

    # Flash algorithm as a hex string
    'instructions': [
    0xE00ABE00, 0x062D780D, 0x24084068, 0xD3000040, 0x1E644058, 0x1C49D1FA, 0x2A001E52, 0x4770D1F2,
    0x4770ba40, 0x4770ba40, 0x4770bac0, 0x4770bac0, 0x0030ea4f, 0x00004770, 0x0030ea4f, 0x00004770,
    0x49052000, 0x49057008, 0x20016008, 0x39264902, 0x002af881, 0x00004770, 0x40054026, 0x40010418,
    0x4004f240, 0xf0006800, 0xb1180001, 0x490b480a, 0xe0026008, 0x4909480a, 0x20056008, 0x60084909,
    0x490a4809, 0x20006208, 0x312a4908, 0x20057008, 0xf8814906, 0x47700026, 0x22205981, 0x40054100,
    0x22204781, 0x40010418, 0x00116310, 0x40054000, 0xf000b510, 0xbd10f811, 0x4604b510, 0xf0004620,
    0xbd10f817, 0x49032000, 0x1e406008, 0x391c4901, 0x47706008, 0x4001041c, 0x2400b510, 0xf948f000,
    0xf0004802, 0x2000f805, 0x0000bd10, 0x03001000, 0x4604b530, 0xf0002500, 0x2004f93b, 0x60084919,
    0x60202000, 0x1c6de007, 0x42854817, 0xf000d303, 0x2001f92f, 0x4813bd30, 0x68001d00, 0x7080f400,
    0x7f80f5b0, 0x480fd007, 0x68001d00, 0x7080f000, 0x7f80f1b0, 0xe007d1e7, 0x3008480a, 0xf0406800,
    0x49081010, 0x60083108, 0x1d004806, 0xf0006800, 0x28001010, 0x4903d1f0, 0xf0006008, 0x2000f909,
    0x0000e7d8, 0x4001041c, 0x00061a80, 0xf000b500, 0xf240f8ff, 0x49171023, 0xf2436008, 0x60082010,
    0x30fff04f, 0x60084914, 0x60081d09, 0x60081d09, 0x60081d09, 0x60081d09, 0x60081d09, 0x60081d09,
    0x60081d09, 0x490b480d, 0x60081d09, 0x600843c0, 0x4908480b, 0x60083118, 0x1d0912c0, 0xf24a6008,
    0x49085001, 0xf7ff8008, 0xf7ffff3b, 0xf000ff49, 0xbd00f8cf, 0x40010400, 0x40010590, 0x01234567,
    0x00080005, 0x400543fe, 0x41f8e92d, 0x460c4605, 0xf6494616, 0x90004040, 0xf24046b0, 0x492f1003,
    0x462f6008, 0x4040f649, 0xbf009000, 0xf8b0f000, 0x0000f8d8, 0x20006038, 0xe00c9000, 0x1c409800,
    0xf6499000, 0x98004140, 0xd3044288, 0xf8a0f000, 0xe8bd2001, 0x482181f8, 0x68001d00, 0x0010f000,
    0xd1eb2810, 0x481de007, 0x68003008, 0x0010f040, 0x3108491a, 0x48196008, 0x68001d00, 0x0010f000,
    0xd0f02810, 0x0804f108, 0x1f241d3f, 0xd2cd2c04, 0x49122000, 0x90006008, 0x9800e00b, 0x90001c40,
    0x4140f649, 0x42889800, 0xf000d303, 0x2001f871, 0x480ae7cf, 0x68001d00, 0x7080f400, 0x7f80f5b0,
    0x4806d007, 0x68001d00, 0x7080f000, 0x7f80f1b0, 0xf000d1e3, 0x2000f85d, 0x0000e7bb, 0x4001041c,
    0x4604b570, 0x4616460d, 0xff50f7ff, 0xbd702000, 0x4604b570, 0x4616460d, 0x46294632, 0xf7ff4620,
    0xbd70ff83, 0x49034802, 0x48036008, 0x47706008, 0xffff0123, 0x40049408, 0xffff3210, 0x4604b510,
    0xfee0f7ff, 0xbd102000, 0x4604b5f0, 0x2300460d, 0x27002600, 0x21004626, 0xf856e007, 0x6810cb04,
    0xd0004584, 0x1d12e004, 0xebb11c49, 0xd3f40f95, 0x4637bf00, 0xe0062300, 0xcb01f817, 0x45845cd0,
    0xe004d000, 0xf0051c5b, 0x42980003, 0xbf00d8f4, 0x0081eb04, 0xbdf04418, 0x49034802, 0x48036088,
    0x47706088, 0xffff0123, 0x40049000, 0xffff3210, 0xf44fb500, 0x68006080, 0x3080f400, 0xf000b908,
    0xf44ff85b, 0x68006080, 0x0001f000, 0xf000b908, 0xbd00f807, 0x1e01bf00, 0x0001f1a0, 0x4770d1fb,
    0x4824b510, 0xb2826800, 0x6080f44f, 0xf3c06800, 0xf44f0481, 0x68006080, 0x2303f3c0, 0x1192b90c,
    0x2c01e008, 0x1292d101, 0x2c02e004, 0x1312d101, 0x1392e000, 0x2001b90b, 0x2000e000, 0xd1012b0f,
    0xe0002101, 0x43082100, 0xf7ffb110, 0xe020ff7b, 0x0001f003, 0xb9e2b118, 0xff74f7ff, 0xf003e019,
    0x28020002, 0x2a01d104, 0xf7ffd113, 0xe010ff6b, 0x0004f003, 0xd1042804, 0xd10a2a02, 0xff62f7ff,
    0xf003e007, 0x28080008, 0x2a03d103, 0xf7ffd101, 0xbd10ff59, 0x40049404, 0x4824b510, 0xb2826840,
    0x6080f44f, 0xf3c06800, 0xf44f4481, 0x68006080, 0x6303f3c0, 0x1192b90c, 0x2c01e008, 0x1292d101,
    0x2c02e004, 0x1312d101, 0x1392e000, 0x2001b90b, 0x2000e000, 0xd1012b0f, 0xe0002101, 0x43082100,
    0xf7ffb110, 0xe020ff69, 0x0001f003, 0xb9e2b118, 0xff62f7ff, 0xf003e019, 0x28020002, 0x2a01d104,
    0xf7ffd113, 0xe010ff59, 0x0004f003, 0xd1042804, 0xd10a2a02, 0xff50f7ff, 0xf003e007, 0x28080008,
    0x2a03d103, 0xf7ffd101, 0xbd10ff47, 0x40049000, 0x00000000
    ],

    # Relative function addresses
    'pc_init': 0x200002c1,
    'pc_unInit': 0x200002fd,
    'pc_program_page': 0x200002d1,
    'pc_erase_sector': 0x200000b9,
    'pc_eraseAll': 0x200000b1,

    'static_base' : 0x20000000 + 0x00000020 + 0x000004b0,
    'begin_stack' : 0x20000700,
    'begin_data' : 0x20000000 + 0x1000,
    'page_size' : 0x1800,
    'analyzer_supported' : False,
    'analyzer_address' : 0x00000000,
    'page_buffers' : [0x20001000, 0x20002800],   # Enable double buffering
    'min_program_length' : 0x1800,

    # Flash information
    'flash_start': 0x3000000,
    'flash_size': 0x1800,
    'sector_sizes': (
        (0x0, 0x1800),
    )
}


class HC32F4A0xG(CoreSightTarget):

    VENDOR = "HDSC"

    MEMORY_MAP = MemoryMap(
        FlashRegion( start=0x00000000, length=0x100000, page_size=0x800, sector_size=0x2000,
                        is_boot_memory=True,
                        algo=FLASH_ALGO),
        FlashRegion( start=0x3000000, length=0x1800, page_size=0x1800, sector_size=0x1800,
                        is_boot_memory=False,
                        is_default=False,
                        algo=FLASH_ALGO_OTP),
        RamRegion(   start=0x1FFFE000, length=0x80000),
        RamRegion(   start=0x200F0000, length=0x1000)
        )

    def __init__(self, session):
        super(HC32F4A0xG, self).__init__(session, self.MEMORY_MAP)
        self._svd_location = SVDFile.from_builtin("HC32F4A0.svd")

    def post_connect_hook(self):
        self.write32(DBGMCU.STCTL, DBGMCU.STCTL_VALUE)
        self.write32(DBGMCU.STCTL1, DBGMCU.STCTL1_VALUE)
        self.write32(DBGMCU.TRACECTL, DBGMCU.TRACECTL_VALUE)


class HC32F4A0xI(CoreSightTarget):

    VENDOR = "HDSC"

    MEMORY_MAP = MemoryMap(
        FlashRegion( start=0x00000000, length=0x200000, page_size=0x800, sector_size=0x2000,
                        is_boot_memory=True,
                        algo=FLASH_ALGO),
        FlashRegion( start=0x3000000, length=0x1800, page_size=0x1800, sector_size=0x1800,
                        is_boot_memory=False,
                        is_default=False,
                        algo=FLASH_ALGO_OTP),
        RamRegion(   start=0x1FFFE000, length=0x80000),
        RamRegion(   start=0x200F0000, length=0x1000)
        )

    def __init__(self, session):
        super(HC32F4A0xI, self).__init__(session, self.MEMORY_MAP)
        self._svd_location = SVDFile.from_builtin("HC32F4A0.svd")

    def post_connect_hook(self):
        self.write32(DBGMCU.STCTL, DBGMCU.STCTL_VALUE)
        self.write32(DBGMCU.STCTL1, DBGMCU.STCTL1_VALUE)
        self.write32(DBGMCU.TRACECTL, DBGMCU.TRACECTL_VALUE)
