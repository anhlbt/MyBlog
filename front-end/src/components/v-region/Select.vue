<script>


import dropdown from 'v-dropdown'
import selector from './selector'

export default {
  name: 'SelectElement',
  components: { dropdown },
  mixins: [selector],
  props: {
    list: {
      type: Array,
      required: true
    },
    blankText: String,
    value: Object
  },
  data () {
    return {
      selected: this.value
    }
  },
  inject: ['disabled', 'blank'],
  watch: {
    value: {
      handler (val) {
        this.selected = val
      },
      deep: true
    }
  },
  computed: {
    content () {
      return (this.selected && this.selected.value)
        ? this.selected.value
        : this.blank ? this.blankText : '&nbsp;'
    }
  },
  render (h) {
    const child = []

    // trigger
    child.push(h('template', { slot: 'caller' }, [
      h('div', {
        class: {
          'rg-select__el': true,
          'rg-select__el--active': this.show,
          'rg-select_el--disabled': this.disabled
        }
      }, [
        h('div', { class: 'rg-select__content form-control' }, this.content), // add form-control
        h('span', { class: 'rg-select__caret' }),
        // console.log(this.content)
      ])
    ]))

    const items = []
    // "Please select" option
    if (this.blank) {
      items.push(h('li', {
        on: {
          click: () => {
            this.pick(null)
          }
        }
      }, this.blankText))
    }
    // list item
    items.push(...this.list.map(val => {
      return h('li', {
        key: val.key,
        class: {
          selected: this.selected && this.selected.key === val.key
        },
        on: {
          click: () => {
            this.pick(val)
          }
        }
      }, val.value)
    }))

    child.push(h('ul', { class: 'rg-select__list' }, items))

    return h('dropdown', {
      ref: 'drop',
      class: 'rg-select',
      props: {
        border: false,
        disabled: this.disabled
      },
      on: {
        show: this.showChange
      }
    }, child)
  },
  methods: {
    pick (val) {
      this.selected = val
      this.$emit('input', val)
      this.close()
    }
  }
}

</script>
<style lang="scss" scoped>
@import "./../../assets/scss/main";

div.rg-selected-container {
	border-top: 1px solid #e6e7e7;
	background-color: #fff;
	border-bottom-left-radius: 2px;
	border-bottom-right-radius: 2px;
	display: inline-block;
	width: 400px;
	position: relative;
}

div.rg-selected-container div.rg-selected-content {
	display: inline-block;
	width: 350px;
}

div.rg-selected-container div.rg-done {
	height: 100%;
	width: 50px;
	display: inline-block;
	text-align: center;
	position: absolute;
	top: 0;
	bottom: 0;
	right: 0;
}

div.rg-selected-container div.rg-done i {
	line-height: 1;
	font-size: 20px;
	top: 50%;
	position: absolute;
	margin-top: -10px;
}

div.rg-select {
	display: inline-block;
	position: relative;
	margin-right: 5px;
}

div.rg-select:last-child {
	margin-right: 0;
}

div.rg-select div.rg-select__el {
	// border: 1px solid #ddd;
	border-radius: 3px;
	transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
	cursor: pointer;
	color: #666;
}

div.rg-select div.rg-select__el div.rg-select__content {
	padding: 6px 30px 6px 15px;
	font-size: 14px;
	display: inline-block;
  min-width: 80px;
  margin-bottom: 20px;
}

// div.rg-select div.rg-select__el:hover {
// 	border: 1px solid #bbb;
// }

div.rg-select div.rg-select__el.rg-select__el--active {
	outline: 0;
	box-shadow: 0 0 0 3px rgba(180,180,180,0.25);
	// border: 1px solid #888;
}

div.rg-select div.rg-select__el.rg-select__el--active span.rg-select__caret {
	transform: rotate(180deg);
}

div.rg-select div.rg-select__el.rg-select_el--disabled {
	// border: 1px solid #eee;
	background-color: #f5f5f5;
	color: #aaa;
}

div.rg-select span.rg-select__caret {
	position: absolute;
	top: 50%;
	right: 12px;
	margin-top: -1px;
	vertical-align: middle;
	display: inline-block;
	width: 0;
	height: 0;
	margin-left: 2px;
	border-top: 4px dashed;
	border-right: 4px solid transparent;
	border-left: 4px solid transparent;
	transition: transform 0.2s ease;
}

ul.rg-select__list {
	list-style: none;
	overflow-y: auto;
	overflow-x: hidden;
	max-height: 300px;
	margin: 0;
	padding: 3px 0;
}

ul.rg-select__list li {
	padding: 3px 10px;
	cursor: pointer;
	min-width: 80px;
	color: #888;
	font-size: 13px;
	line-height: 1.5;
}

ul.rg-select__list li:hover {
	background-color: #f5f7fa;
}

ul.rg-select__list li.selected {
	background-color: #e4eaee;
	color: #000;
}

</style>