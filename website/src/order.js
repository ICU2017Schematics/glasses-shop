import EventBus from './event-bus.js'
const axios = require('axios')
const config = {
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
}

export default class Order {
    constructor(order) {
        this.shipping = order ? order.shipping : {}
        this.email = order ? order.email : ''
        this.id = order ? order.id : ''
        this.lineitems = order ? order.lineitems : []
        this.total = order ? order.total : 0
    }

    post(API_ENDPOINT) {
        if (this.id == '') return

        const self = this
        const data = {
            order: this
        }
        axios.post(API_ENDPOINT + '/orders', data, config).then(res => {
            EventBus.$emit('ORDER_POSTED', {order: self, tracking_url: res.data.tracking_url})
        })
    }
}
