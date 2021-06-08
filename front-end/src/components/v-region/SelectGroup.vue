// import './styles/select.styl'
// import './styles/icons.styl'
// import './styles/group.styl'
<script>
import { PROVINCE_LEVEL } from './constants'

import data from './data'
import method from './method'
import select from './Select'

export default {
  name: 'SelectGroup',
  mixins: [data, method],
  components: {
    'r-select': select
  },
  props: {
    blank: {
      type: Boolean,
      default: true
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  inheritAttrs: false,
  provide () {
    return {
      disabled: this.disabled,
      blank: this.blank
    }
  },
  render (h) {
    const child = []
    const { province, city, area, town } = this.region

    child.push(this.build(h, {
      list: this.listProvince,
      model: province,
      blank_text: "Chọn Tỉnh: ",
      callback: val => {
        this.region.province = val
      }
    }))

    if (this.city) {
      child.push(this.build(h, {
        list: this.listCity,
        model: city,
        blank_text: "Chọn Quận/Huyện: ",
        callback: val => {
          this.region.city = val
        }
      }))
    }
    if (this.city && this.area) {
      child.push(this.build(h, {
        list: this.listArea,
        model: area,
        blank_text: "Chọn Phường/Xã: ",
        callback: val => {
          this.region.area = val
        }
      }))
    }
    if (this.city && this.area && this.town) {
      child.push(this.build(h, {
        list: this.listTown,
        model: town,
        callback: val => {
          this.region.town = val
        }
      }))
    }

    return h('div', child)
  },
  methods: {
    build (h, { list, model, blank_text, callback }) {
      return h('r-select', {
        props: {
          'blank-text': blank_text, //this.lang.pleaseSelect,
          list: list
        },
        attrs: {
          value: model
        },
        on: {
          input: val => {
            callback(val)
            this.change()
          }
        }
      })
    }
  }
}
</script>

