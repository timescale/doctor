# Copyright 2023 Timescale, Inc.
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

"""Rules for indexes."""

from dataclasses import dataclass

import doctor

UNUSED_QUERY = """
SELECT relid::regclass as relation,
       indexrelname,
       pg_size_pretty(pg_relation_size(i.indexrelid)) AS index_size
FROM pg_stat_user_indexes ui JOIN pg_index i USING (indexrelid)
WHERE NOT indisunique
  AND idx_scan = 0
  AND schemaname NOT LIKE '_timescaledb%';
"""

@doctor.register
@dataclass
class UnusedIndex(doctor.Rule):
    """Find all unused indexes."""

    query: str = UNUSED_QUERY
    message: str = "index '{indexrelname}' on table '{relation}' is not used"
    detail: str = "Index {indexrelname} is not used and occupied {index_size}."
    hint: str = ("Since the index '{indexrelname}' on table '{relation}' is not used,"
                 " you can remove it.")
