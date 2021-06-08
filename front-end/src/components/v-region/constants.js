/**
 * Plugin types
 */
export const TEXT = 'text'
export const SELECT = 'select'
export const GROUP = 'group'
export const COLUMN = 'column'
export const CITY = 'city'

export const PROVINCE_LEVEL = 0
export const CITY_LEVEL = 1
export const AREA_LEVEL = 2
export const TOWN_LEVEL = 3

export const LEVELS = [
  { index: PROVINCE_LEVEL, title: 'Tỉnh' },
  { index: CITY_LEVEL, title: 'Quận/Huyện' },
  { index: AREA_LEVEL, title: 'Phường/Xã' },
  { index: TOWN_LEVEL, title: 'Khu phố, Đường' }
]

export const PROVINCE_KEY = 'province'
export const CITY_KEY = 'city'
export const AREA_KEY = 'area'
export const TOWN_KEY = 'town'

export const LEVEL_LIST = [PROVINCE_KEY, CITY_KEY, AREA_KEY, TOWN_KEY]
