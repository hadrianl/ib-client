import VueI18n from "vue-i18n"
import Vue from "vue"

Vue.use(VueI18n)

const messages = {
    en: {
        nav: {
            trade: "Trade",
            market: "Market",
            analysis: "Analysis",
            extra: "Extra",
        },
        button: {
            connect: "Connect",
            stop: "Stop",
            buy: "Buy",
            sell: "Sell",
            trail: "Trail",
            notSet: "Not Set",
            reset: "Reset",
            cancelAllOrders: "cancelAllOrders",
            predict: "predict",
            VaR: "VaR",
        },
        cost: {
            refCost: "Reference cost",
            openCost: "Open cost",
            sessCost: "Session cost",
            totalCost: "Total cost",
        },
        orderTab: {
            stopLoss: "StopLimit",
            trailStop: "TrailStop",
            maTrigger: "MATrigger",
            limit: "Limit",
            bracket: "Bracket",
        },
        mainTab: {
            order: "ORDER",
            fill: "FILL",
            portfolio: "PORTFOLIO",
            position: "POSITION",
            account: "ACCOUNT",
        },
        analysisTab: {
            trend: "TREND",
            heatmap: "HEATMAP"
        },
        placeHolder: {
            contractInput: "please input contract",
            triggerType: "trigger type"
        },
        connState: {
            connected: "Connected",
            disconnected: "Disconnected",
        },
        utils: {
            setCloseAll: "Set Close All Params"
        }
    },
    zh: {
        nav: {
            trade: "交易",
            market: "行情",
            analysis: "分析",
            extra: "附加",
        },
        button: {
            connect: "连接",
            stop: "停止",
            buy: "买",
            sell: "卖",
            trail: "追踪",
            notSet: "未设置",
            reset: "重置",
            cancelAllOrders: "取消全部订单",
            predict: "预测",
            VaR: "在险价值",
        },
        cost: {
            refCost: "参考成本",
            openCost: "开仓成本",
            sessCost: "会话成本",
            totalCost: "总成本",
        },
        orderTab: {
            stopLoss: "停止限价",
            trailStop: "移动止损",
            maTrigger: "均线触发",
            limit: "限价",
            bracket: "包括单",
        },
        mainTab: {
            order: "订单",
            fill: "成交",
            portfolio: "组合",
            position: "持仓",
            account: "账户",
        },
        analysisTab: {
            trend: "贡献度趋势",
            heatmap: "贡献度热力图"
        },
        placeHolder: {
            contractInput: "输入合约",
            triggerType: "触发类型"
        },
        connState: {
            connected: "已连接",
            disconnected: "未连接",
        },
        utils: {
            setCloseAll: "设置一键平仓参数"
        }
    },
}


const i18n = new VueI18n({
    locale: 'zh',
    messages: messages
})

export default i18n