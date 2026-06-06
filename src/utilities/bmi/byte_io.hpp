/*
Author: Nels Frazier
Copyright (C) 2025 Lynker
------------------------------------------------------------------------
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
------------------------------------------------------------------------
INTERNAL — implementation detail of wire_format::RecordPrefix.

This header provides the little-endian byte-level read/write
primitives that `wire_format::write_record_prefix` and
`read_record_prefix` use to encode the prefix's integer fields. It
is not a general-purpose serialization utility, has no API contract
of its own, and must not be used outside `wire_format.hpp`. The
design rationale for field-level LE I/O (why not boost archives,
the cross-host portability claims the wire format makes, the
two's-complement assumption and its run-host canary tests, etc.)
lives with the wire format itself — see `wire_format.hpp`.

Visibility is enforced by include-path discipline: this header is
only on the PRIVATE include path of the `ngen_bmi_protocols`
library's own translation units and of the `test_bmi_protocols`
test target. It is never exported via `target_include_directories(PUBLIC ...)`.
*/
#pragma once

#include <cstdint>
#include <cstring>
#include <istream>
#include <ostream>

namespace models {
namespace bmi {
namespace protocols {
namespace serialization {
namespace byte_io {

// Little-endian extraction / reassembly mechanics:
//
// (v & 0xFF) keeps the lowest 8 bits — the byte that goes first on
// disk. A right shift then brings the next byte down into the lowest
// position; repeat for each additional byte the type holds,
// incrementing the shift by 8 each time. Reading inverts this: the
// lowest byte on disk goes into the low-byte position of the result
// (no shift), and each subsequent byte is widened to the target
// unsigned type and shifted left by 8 more than the previous, then
// OR'd together.
//
// The 0xFF mask in the write path is redundant with the
// `static_cast<char>` that follows (the cast already truncates to 8
// bits) but is kept as an explicit statement of intent on the line.
// The widening cast in the read path is required: a raw
// `unsigned char << 8` auto-promotes to int, losing the
// explicit-target-type semantics.
//
// Signed types travel through their unsigned bit-pattern via
// `std::memcpy`. This assumes two's-complement signed representation
// — see wire_format.hpp for the assumption's role in the wire
// format's portability claim and for the run-host canary tests that
// verify it.
//
// The `// clang-format off` / `on` markers in the write_uN_le and
// read_uN_le bodies below keep one byte (or one OR'd operand) per
// line. Auto-formatting would happily pack them two-per-line when
// they fit in the column limit, which loses the at-a-glance
// vertical verification of the LE pattern — the very property
// these helpers exist to make obvious. The protection is per-
// function so the surrounding code (if/return, casts, etc.)
// formats normally.

inline void write_u8(std::ostream& out, uint8_t v) {
    out.put(static_cast<char>(v));
}

inline bool read_u8(std::istream& in, uint8_t& v) {
    char c;
    if (!in.get(c)) return false;
    v = static_cast<uint8_t>(c);
    return true;
}

inline void write_u16_le(std::ostream& out, uint16_t v) {
    // clang-format off
    const char bytes[2] = {
        static_cast<char>( v        & 0xFF),
        static_cast<char>((v >> 8)  & 0xFF),
    };
    // clang-format on
    out.write(bytes, 2);
}

inline bool read_u16_le(std::istream& in, uint16_t& v) {
    unsigned char bytes[2];
    if (!in.read(reinterpret_cast<char*>(bytes), 2)) return false;
    if (in.gcount() != 2) return false;
    // The outer static_cast<uint16_t> is the demote-back step that
    // read_u32_le and read_u64_le don't need. `uint16_t << 8`
    // promotes to int because uint16_t is smaller than int, so the
    // shift result is int-typed; the cast narrows it back and
    // suppresses any -Wconversion / -Wnarrowing warning at the OR.
    // clang-format off
    v = static_cast<uint16_t>(bytes[0])
      | static_cast<uint16_t>(static_cast<uint16_t>(bytes[1]) << 8);
    // clang-format on
    return true;
}

inline void write_u32_le(std::ostream& out, uint32_t v) {
    // clang-format off
    const char bytes[4] = {
        static_cast<char>( v        & 0xFF),
        static_cast<char>((v >> 8)  & 0xFF),
        static_cast<char>((v >> 16) & 0xFF),
        static_cast<char>((v >> 24) & 0xFF),
    };
    // clang-format on
    out.write(bytes, 4);
}

inline bool read_u32_le(std::istream& in, uint32_t& v) {
    unsigned char bytes[4];
    if (!in.read(reinterpret_cast<char*>(bytes), 4)) return false;
    if (in.gcount() != 4) return false;
    // clang-format off
    v = static_cast<uint32_t>(bytes[0])
      | (static_cast<uint32_t>(bytes[1]) << 8)
      | (static_cast<uint32_t>(bytes[2]) << 16)
      | (static_cast<uint32_t>(bytes[3]) << 24);
    // clang-format on
    return true;
}

inline void write_u64_le(std::ostream& out, uint64_t v) {
    // clang-format off
    const char bytes[8] = {
        static_cast<char>( v        & 0xFF),
        static_cast<char>((v >> 8)  & 0xFF),
        static_cast<char>((v >> 16) & 0xFF),
        static_cast<char>((v >> 24) & 0xFF),
        static_cast<char>((v >> 32) & 0xFF),
        static_cast<char>((v >> 40) & 0xFF),
        static_cast<char>((v >> 48) & 0xFF),
        static_cast<char>((v >> 56) & 0xFF),
    };
    // clang-format on
    out.write(bytes, 8);
}

inline bool read_u64_le(std::istream& in, uint64_t& v) {
    unsigned char bytes[8];
    if (!in.read(reinterpret_cast<char*>(bytes), 8)) return false;
    if (in.gcount() != 8) return false;
    // clang-format off
    v = static_cast<uint64_t>(bytes[0])
      | (static_cast<uint64_t>(bytes[1]) << 8)
      | (static_cast<uint64_t>(bytes[2]) << 16)
      | (static_cast<uint64_t>(bytes[3]) << 24)
      | (static_cast<uint64_t>(bytes[4]) << 32)
      | (static_cast<uint64_t>(bytes[5]) << 40)
      | (static_cast<uint64_t>(bytes[6]) << 48)
      | (static_cast<uint64_t>(bytes[7]) << 56);
    // clang-format on
    return true;
}

inline void write_i32_le(std::ostream& out, int32_t v) {
    uint32_t u;
    std::memcpy(&u, &v, sizeof(u));
    write_u32_le(out, u);
}

inline bool read_i32_le(std::istream& in, int32_t& v) {
    uint32_t u;
    if (!read_u32_le(in, u)) return false;
    std::memcpy(&v, &u, sizeof(v));
    return true;
}

inline void write_i64_le(std::ostream& out, int64_t v) {
    uint64_t u;
    std::memcpy(&u, &v, sizeof(u));
    write_u64_le(out, u);
}

inline bool read_i64_le(std::istream& in, int64_t& v) {
    uint64_t u;
    if (!read_u64_le(in, u)) return false;
    std::memcpy(&v, &u, sizeof(v));
    return true;
}

} // namespace byte_io
} // namespace serialization
} // namespace protocols
} // namespace bmi
} // namespace models
