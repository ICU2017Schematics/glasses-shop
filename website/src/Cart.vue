<template>
    <div id="cart">
        <h1>Your Shopping Cart</h1>
        <table class="table table-striped table-bordered">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Retail Price</th>
                    <th>Sale Price</th>
                    <th>Quantity</th>
                    <th>Subtotal</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="item in cart.lineitems">
                    <td>{{ item.name }}</td>
                    <td>$ <s>{{ item.retail_price }}</s></td>
                    <td><strong>$ {{ item.sale_price }}</strong></td>
                    <td><input type="number" min="0" max="10" v-model="item.qty"></td>
                    <td><strong>$ {{ subtotal(item) }}</strong></td>
                </tr>
                <tr>
                    <td colspan="5">
                        <p class="pull-right">Total:
                            <strong>$ {{ total }}</strong>
                        </p>
                    </td>
                </tr>
            </tbody>
        </table>
        <button class="btn btn-primary" v-on:click="checkout">Checkout</button>
    </div>
</template>

<script>
import Order from './order.js'

export default {
  data() {
      return { }
  },
  computed: {
    total() {
        let total = 0
        this.cart.lineitems.forEach(item => {
            total += item.sale_price * item.qty
        })

        return total
    }
  },
  methods: {
    subtotal(item) {
        return item.qty * item.sale_price
    },
    checkout() {
        const self = this
        let handler = StripeCheckout.configure({
            key: 'pk_test_6pRNASCoBOKtIshFeQd4XMUh',
            image: 'https://cdn1.iconfinder.com/data/icons/cool-kiddo-1/100/geek_brainy_studious_specs-256.png', //https://stripe.com/img/documentation/checkout/marketplace.png',
            locale: 'auto',
            token(token) {
                const order = new Order({
                    shipping: {
                        name: token.card.name,
                        address: token.card.address_line1,
                        city: token.card.address_city,
                        state: token.card.address_state,
                        zipcode: token.card.address_zip
                    },
                    email: token.email,
                    id: token.id.replace('tok_', ''),
                    lineitems: [],
                    total: 0
                })
                self.cart.lineitems.forEach(item => {
                    order.lineitems.push({
                        product_id: item.product_id,
                        name: item.name,
                        qty: item.qty,
                        price: item.sale_price,
                        subtotal: item.qty * item.sale_price * 1
                    })
                })
                order.lineitems.forEach(item => {
                    order.total += item.subtotal
                })
                
                order.post(self.API_ENDPOINT)

                handler.close()
                self.$router.push('/thankyou/' + token.id.replace('tok_', ''))
            }
        })

        handler.open({
            name: 'Glasses 4 U',
            description: 'checkout',
            zipCode: true,
            billingAddress: true,
            shippingAddress: true,
            amount: self.total * 100
        });
    }
  }
}
</script>
