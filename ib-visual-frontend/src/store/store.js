import Vuex from 'vuex'
import Vue from 'vue'

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
        currentContract: null,
        contractsList: [],
        isConnected: false
    },
    mutations:{
        selectContract(state, contract) {
            console.log(contract)
            state.currentContract = contract
        },

        addContract(state, contract){
            var flag = true
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

        setConnectState(state, b) {
            state.isConnected = b
        }
    }
})


  export default store