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
        fillsList: [],
        isConnected: false
    },
    getters: {
        availableTradesList: state => {
            return state.tradesList.filter(t => ['Cancelled', 'ApiCancelled'].indexOf(t.orderStatus.status) == -1)
        },
        currentFillsList: state => {
            if(!state.currentContract){
                return []
            }
            return state.fillsList.filter(f => f.contract.conId === state.currentContract.conId)
        },
        currenTradesList: state => {
            if(!state.currentContract){
                return []
            }
            return state.tradesList.filter(t => t.contract.conId == state.currentContract.conId)
        },
        currentOpenCost: (state, getters) => {
            const fills = getters.currentFillsList
            if(!state.currentContract || !fills){
                return [0, 0]
            }

            let arr = [[0, 0]]  // set [0, 0] 
            let priceSum = 0
            let posSum = 0
            let sessionBeginIndex = 0
            for(let i in fills){
                if(posSum==0){
                    sessionBeginIndex = i
                }
                const f = fills[i]
                const size = f.execution.side == 'BOT'?f.execution.shares:-f.execution.shares
                priceSum += f.execution.price * size
                posSum += size
                arr.push([priceSum, posSum])
            }
            
            const lastSession = arr.slice(sessionBeginIndex)
            // lastSession.reverse()
            const fristState = lastSession[0]
            const lastState = lastSession[lastSession.length - 1]
            const lastPos = lastState[1]
            let openCostState = [lastState[0] - fristState[0], lastState[1] - fristState[1]]
            // const pos = openCostState[1]
            for(let i in lastSession){
                let currentState = lastSession[i]
                if (Math.abs(currentState[1])>=Math.abs(lastPos)){
                    let value_diff = currentState[0]-fristState[0]
                    let pos_diff = currentState[1] - fristState[1]
                    openCostState = [(pos_diff?value_diff/pos_diff:value_diff)*lastPos, lastPos]
                    break
                }
            }

            return openCostState
        },
        currentSessionCost: (state, getters) => {
            const fills = getters.currentFillsList
            if(!state.currentContract || !fills){
                return [0, 0]
            }

            let arr = [[0, 0]]
            let priceSum = 0
            let posSum = 0
            let sessionBeginIndex = 0
            for(let i in fills){
                if(posSum==0){
                    sessionBeginIndex = i
                }

                const f = fills[i]
                const size = f.execution.side == 'BOT'?f.execution.shares:-f.execution.shares
                priceSum += f.execution.price * size
                posSum += size
                arr.push([priceSum, posSum])
            }

            const lastSession = arr.slice(sessionBeginIndex)
            const fristState = lastSession[0]
            const lastState = lastSession[lastSession.length - 1]
            // const lastState = arr[arr.length -1]
            // let fristState = arr[0]
 
            // for(let i = arr.length - 1; i >=0; i--){
            //     if(arr[i][1] == 0){
            //         fristState = arr[i]
            //         break
            //     }
            // }

            return [lastState[0] - fristState[0], lastState[1] - fristState[1]]

        },
        currentTotalCost: (state, getters) => {
            const fills = getters.currentFillsList
            if(!state.currentContract || !fills){
                return [0, 0]
            }

            let arr = []
            let priceSum = 0
            let posSum = 0
            for(let f of fills){
                let size = f.execution.side == 'BOT'?f.execution.shares:-f.execution.shares
                priceSum += f.execution.price * size
                posSum += size
                arr.push([priceSum, posSum])
            }

            return arr[arr.length - 1]
        }
    },
    mutations:{
        selectContract(state, contract) {
            console.log(`selectContract: ${contract}`)
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

            state.tradesList.push(trade)
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
    
            state.positionsList.push(position)
        },

        initFills(state, fills) {
            fills.forEach((v, i) => fills[i].time = new Date(v.time).getTime() / 1000)
            fills.sort((a, b) => a.time - b.time)
            state.fillsList = fills
        },

        updateFill(state, fill) {
            // for(let i in state.fillsList){
            //     if(state.fillsList[i].execution.execId === fill.execution.execId){
            //         state.fillsList.splice(i, 1, fill)
            //         return
            //     }
            // }

            state.fillsList.push(fill)
        },

        setConnectState(state, b) {
            state.isConnected = b
        }
    }
})


  export default store