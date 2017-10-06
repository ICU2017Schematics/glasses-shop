import EventBus from './event-bus.js'
const axios = require('axios')

export default class CartController {
    constructor(API_ENDPOINT) {
        console.log('>>> CREATE cart')
        this.API_ENDPOINT = API_ENDPOINT
        this.token = ''
        this.lineitems = []
        this.created = 0
        this.session = ''

        this.getCart()
    }

    getCart() {
        let session = localStorage.getItem('eyeglasses.session')
        if (session == null) {
            session = Date.now()
            localStorage.setItem('eyeglasses.session', session)
        }
        this.session = session

        const config = {
            headers: {
                'Accept': 'application/json'
            }
        }
        const self = this
        axios.get(this.API_ENDPOINT + '/cart/' + session, config).then(res => {
            self.token = res.data.cart_token
            self.created = res.data.created
            for (const item in res.data.lineitems) {
                self.lineitems.push(res.data.lineitems[item])
            }
            EventBus.$emit('CART_UPDATED', self.lineitems)
        })                
    }

    addToCart(product) { 
        const url = this.API_ENDPOINT + '/cart/' + this.session
        const data = {
            lineitem: {
                product_id: product.product_id,
                name: product.name,
                retail_price: product.retail_price,
                sale_price: product.sale_price
            }
        }
        const config = {
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Cart-Token': this.token
            },
        }
        
        const self = this
        axios.post(url, data, config).then(function(res) {
            // lineitems is an object to iterate over. convert to array for viewmodel
            self.lineitems.length = 0
            for (const item in res.data.lineitems) {
                self.lineitems.push(res.data.lineitems[item])
            }
            
            EventBus.$emit('CART_UPDATED', self.lineitems)
        })
    }

    delete() {
        const self = this
        const url = this.API_ENDPOINT + '/cart/' + this.session
        const config = {
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Cart-Token': this.token
            },
        }
        
        axios.delete(url, config).then(function(res) {
            const num_items = self.lineitems.length
            for (let i=0; i<num_items; i++) {
                self.lineitems.pop()
            }
            EventBus.$emit('CART_DELETED', {})
        })        
    }
}
