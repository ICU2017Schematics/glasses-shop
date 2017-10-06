<template>
    <div id="cart-button">
        <ul class="nav nav-pills navbar-right">
            <li role="presentation"><router-link to="/cart" id="show-cart"><button class="btn btn-primary"><span class="badge"><i class="glyphicon glyphicon-shopping-cart"></i><span id="cart-amount">{{ num_items }}</span></span> Cart</button></router-link></li>
        </ul>
    </div>  
</template>

<script>
import EventBus from './event-bus.js'
export default {
    name: 'CartButton',
    data() { 
        return {}
    },
    created() {
        EventBus.$on('CART_UPDATED', lineitems => {
        })

        EventBus.$on('CART_DELETED', lineitems => {
            this.cart.getCart()
            this.$forceUpdate()
        })
    },
    computed: {
        num_items() { 
            let total = 0
            this.cart.lineitems.forEach(item => { total += 1 * item.qty })
            return total
        }
    }
}
</script>
