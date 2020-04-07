import Vuex from 'vuex'
import Vue from 'vue'

Vue.use(Vuex)

export function orderKey(orderId, permId, clientId) {
    if (orderId <= 0) {
        return String(permId)
    }else{
        return String(clientId) + String(orderId)
    }
}

export function is_same_key(n_trade, o_trade) {
    var nKey = orderKey(n_trade.order.orderId, n_trade.order.permId, n_trade.order.clientId)
    var oKey = orderKey(o_trade.order.orderId, o_trade.order.permId, o_trade.order.clientId)
    
    return nKey == oKey
}


const store = new Vuex.Store({
    state: {
        currentContract: null,
        contractsList: [],
        tradesList: [],
        positionsList: [],
        isConnected: false
    },
    getters: {
        availableTradesList: state => {
            return state.tradesList.filter(t => ['Cancelled', 'ApiCancelled'].indexOf(t) == -1)
        }
    },
    mutations:{
        selectContract(state, contract) {
            console.log(contract)
            state.currentContract = contract
        },

        addContract(state, contract){
            let flag = true
            state.contractsList.forEach(element => {
                if (element.conId === contract.conId){
                    flag = false
                }
            })
            if (flag){
                state.contractsList.push(contract)
            }
        },

        clearContract(state) {
            state.currentContract = null
        },

        initTrades(state, trades) {
            state.tradesList = trades
        },

        updateTrade(state, trade) {
            for (let i in state.tradesList){
                if (is_same_key(trade, state.tradesList[i])){
                    state.tradesList.splice(i, 1, trade)
                    return
                }
            }

            state.tradesList.unshift(trade)
        },

        initPositions(state, positions) {
            state.positionsList = positions
        },

        updatePosition(state, position) {
            for (let i in state.positionsList){
                if (state.positionsList[i].conId === position.conId){
                    state.positionsList.splice(i, 1, position)
                        return
                    }
                }
    
            state.positionsList.unshift(position)
        },

        setConnectState(state, b) {
            state.isConnected = b
        }
    }
})


  export default store