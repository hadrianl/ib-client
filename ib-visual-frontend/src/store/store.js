import Vuex from 'vuex'
import Vue from 'vue'

Vue.use(Vuex)

export function orderKey({orderId, permId, clientId=0}) {
    if (orderId <= 0) {
        return String(permId)
    }else{
        return String(clientId) + String(orderId)
    }
}

export function is_same_key(n_trade, o_trade) {
    var nKey = orderKey(n_trade.order)
    var oKey = orderKey(o_trade.order)

    return nKey == oKey
}


const store = new Vuex.Store({
    state: {
        currentContract: null,
        contractsList: [],
        tradesList: [],
        positionsList: [],
        portfolioList: [],
        fillsList: [],
        accountValues: [],
        isConnected: false
    },
    getters: {
        availableTradesList: state => {
            return state.tradesList.filter(t => ['Cancelled', 'ApiCancelled'].indexOf(t.orderStatus.status) == -1)
        },
        currentPortfolio: state => {
            for (let i in state.portfolioList){
                if (state.portfolioList[i].contract.conId === state.currentContract.conId){
                        return state.portfolioList[i]
                    }
                }
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
        // currentAvailableTradesList: (state, getters) => {
        //     return getters.currenTradesList.filter(t => ['Cancelled', 'ApiCancelled'].indexOf(t.orderStatus.status) == -1)
        // },
        currentOpenCost: (state, getters) => {
            const fills = getters.currentFillsList
            if(!state.currentContract || fills.length == 0){
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
            if(!state.currentContract || fills.length == 0){
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

            return [lastState[0] - fristState[0], lastState[1] - fristState[1]]

        },
        currentTotalCost: (state, getters) => {
            const fills = getters.currentFillsList
            if(!state.currentContract || fills.length == 0){
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
                if (state.positionsList[i].contract.conId === position.contract.conId){
                    state.positionsList.splice(i, 1, position)
                        return
                    }
                }
    
            state.positionsList.push(position)
        },

        initPortfolio(state, portfolio) {
            state.portfolioList = portfolio
        },

        updatePortfolio(state, portfolioItem) {
            for (let i in state.portfolioList){
                if (state.portfolioList[i].contract.conId === portfolioItem.contract.conId){
                    state.portfolioList.splice(i, 1, portfolioItem)
                        return
                    }
                }
    
            state.portfolioList.push(portfolioItem)
        },

        initFills(state, fills) {
            state.fillsList = fills
            .map(f => {
                    f.time = new Date(f.time).getTime() / 1000 + 28800
                    return f
                    }
                )
            .sort((a, b) => a.time - b.time)
        },

        updateFill(state, fill) {
            fill.time = new Date(fill.time).getTime() / 1000 + 28800
            for(let i in state.fillsList){
                if(state.fillsList[i].execution.execId == fill.execution.execId){
                    state.fillsList.splice(i, 1, fill)
                    return
                }
            }

            state.fillsList.push(fill)
        },

        initAccountValues(state, values) {
            state.accountValues = values
        },

        updateAccountValue(state, v) {
            for (let i in  state.accountValues){
                if (state.accountValues[i].account === v.account && state.accountValues[i].tag === v.tag && state.accountValues[i].currency === v.currency){
                    state.accountValues.splice(i, 1, v)
                    return
                }
            }
            state.accountValues.push(v)
        },

        setConnectState(state, b) {
            state.isConnected = b
        }
    }
})


  export default store