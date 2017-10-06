<template>
    <div id="thankyou">
        <h3>Thank you for your order. Your order number is <strong>{{ token }}</strong>. <a :href="tracking_url">Click here</a> to track the status of your order.</h3>

        <h3>Your Order</h3>

        <table class="table table-striped table-bordered">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Price</th>
                    <th>Quantity</th>
                    <th>Subtotal</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="item in order.lineitems">
                    <td>{{ item.name }}</td>
                    <td><strong>$ {{ item.price }}</strong></td>
                    <td>{{ item.qty }}</td>
                    <td><strong>$ {{ item.subtotal }}</strong></td>
                </tr>
                <tr>
                    <td colspan="4">
                        <p class="pull-right">Total:
                            <strong>$ {{ order.total }}</strong>
                        </p>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import EventBus from './event-bus.js'
import Order from './order.js'

export default {
  data() {
    return { 
        token: this.$route.params.id,
        order: new Order(),
        tracking_url: ''
    }
  },
  created() {
      const self = this
      EventBus.$on('ORDER_POSTED', (res) => {
        self.order.id = res.order.id
        self.order.email = res.order.email
        self.order.shipping = res.order.shipping
        self.order.total = res.order.total
        res.order.lineitems.forEach(item => {
            self.order.lineitems.push(item)
        })
        self.tracking_url = res.tracking_url
      })
  },
  mounted() {
      this.cart.delete()
  }
}
</script>
