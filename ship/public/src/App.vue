<template>
  <div id="app">
    <h2>Order #{{ order.id }}</h2>
    <h3>Status: {{ order_status }}</h3>
    <div class="panel panel-default">
      <div class="panel-heading">
        <h3 class="panel-title">Shipping Information</h3>
      </div>
      <div class="panel-body" v-if="order.id">
        <p><strong>Email: </strong>{{ order.email }}</p>
        <p><strong>Address: </strong>{{ order.shipping.address }}</p>
        <p><strong>City: </strong>{{ order.shipping.city }}</p>
        <p><strong>State: </strong>{{ order.shipping.state }}</p>
        <p><strong>Zipcode: </strong>{{ order.shipping.zipcode }}</p>
      </div>
    </div>

    <div class="panel panel-default">
      <div class="panel-heading">
        <h3 class="panel-title">Order Information</h3>
      </div>
      <div class="panel-body">
        <table class="table table-striped table-bordered">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Price</th>
                    <th>Quantity</th>
                    <th>Subtotal</th>
                </tr>
            </thead>
            <tbody v-if="order.id">
                <tr v-for="item in order.lineitems">
                    <td>{{ item.name }}</td>
                    <td><strong>$ {{ item.price }}</strong></td>
                    <td>{{ item.qty }}</td>
                    <td><strong>$ {{ item.subtotal }}</strong></td>
                </tr>
                <tr>
                    <td colspan="4">
                        <h4 class="pull-right">Total:
                            <strong>$ {{ order.total }}</strong>
                        </h4>
                    </td>
                </tr>
            </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
const axios = require('axios')

export default {
  name: 'app',
  data () {
    return {
      order: {
        lineitems: [],
        shipping: {},
        email: '',
        id: '',
        status: 0,
        total: 0
      }
    }
  },
  created() {
    const self = this
    const url = '/api/orders/' + window.location.pathname.split('/')[2]
    const config = {
      headers: {
        'Accept': 'application/json'
      }
    }
    axios.get(url, config).then(res => {
      const order = res.data
      self.order.shipping = order.shipping
      self.order.lineitems = order.lineitems
      self.order.email = order.email
      self.order.id = order.id
      self.order.total = order.total
      self.order.status = order.status
    })
  },
  computed: {
    order_status() {
      const text = [
        "Preparing order items",
        "Shipping order",
        "FedEx received order... scheduling delivery",
        "En route",
        "En route",
        "Out for delivery",
        "Delivered"
      ]
      return this.order.id ? text[this.order.status % text.length] : ""
    }
  }
}
</script>
