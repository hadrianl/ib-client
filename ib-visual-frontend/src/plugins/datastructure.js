const UNSET_INTEGER = 2 ** 31 - 1
const UNSET_DOUBLE = 1.7976931348623157e+308

class Order {
    constructor() {
        this.orderId = 0
        this.clientId = 0
        this.permId = 0
        this.action = ''
        this.totalQuantity = 0.0
        this.orderType = ''
        this.lmtPrice = UNSET_DOUBLE
        this.auxPrice = UNSET_DOUBLE
        this.tif = ''
        this.activeStartTime = ''
        this.activeStopTime = ''
        this.ocaGroup = ''
        this.ocaType = 0
        this.orderRef = ''
        this.transmit  = true
        this.parentId = 0
        this.blockOrder  = false
        this.sweepToFill  = false
        this.displaySize = 0
        this.triggerMethod = 0
        this.outsideRth  = false
        this.hidden  = false
        this.goodAfterTime = ''
        this.goodTillDate = ''
        this.rule80A = ''
        this.allOrNone  = false
        this.minQty = UNSET_INTEGER
        this.percentOffset = UNSET_DOUBLE
        this.overridePercentageConstraints  = false
        this.trailStopPrice = UNSET_DOUBLE
        this.trailingPercent = UNSET_DOUBLE
        this.faGroup = ''
        this.faProfile = ''
        this.faMethod = ''
        this.faPercentage = ''
        this.designatedLocation = ''
        this.openClose = "O"
        this.origin = 0
        this.shortSaleSlot = 0
        this.exemptCode = -1
        this.discretionaryAmt = 0
        this.eTradeOnly  = true
        this.firmQuoteOnly  = true
        this.nbboPriceCap = UNSET_DOUBLE
        this.optOutSmartRouting  = false
        this.auctionStrategy = 0
        this.startingPrice = UNSET_DOUBLE
        this.stockRefPrice = UNSET_DOUBLE
        this.delta = UNSET_DOUBLE
        this.stockRangeLower = UNSET_DOUBLE
        this.stockRangeUpper = UNSET_DOUBLE
        this.randomizePrice  = false
        this.randomizeSize  = false
        this.volatility = UNSET_DOUBLE
        this.volatilityType = UNSET_INTEGER
        this.deltaNeutralOrderType = ''
        this.deltaNeutralAuxPrice = UNSET_DOUBLE
        this.deltaNeutralConId = 0
        this.deltaNeutralSettlingFirm = ''
        this.deltaNeutralClearingAccount = ''
        this.deltaNeutralClearingIntent = ''
        this.deltaNeutralOpenClose = ''
        this.deltaNeutralShortSale  = false
        this.deltaNeutralShortSaleSlot = 0
        this.deltaNeutralDesignatedLocation = ''
        this.continuousUpdate  = false
        this.referencePriceType = UNSET_INTEGER
        this.basisPoints = UNSET_DOUBLE
        this.basisPointsType = UNSET_INTEGER
        this.scaleInitLevelSize = UNSET_INTEGER
        this.scaleSubsLevelSize = UNSET_INTEGER
        this.scalePriceIncrement = UNSET_DOUBLE
        this.scalePriceAdjustValue = UNSET_DOUBLE
        this.scalePriceAdjustInterval = UNSET_INTEGER
        this.scaleProfitOffset = UNSET_DOUBLE
        this.scaleAutoReset  = false
        this.scaleInitPosition = UNSET_INTEGER
        this.scaleInitFillQty = UNSET_INTEGER
        this.scaleRandomPercent  = false
        this.scaleTable = ''
        this.hedgeType = ''
        this.hedgeParam = ''
        this.account = ''
        this.settlingFirm = ''
        this.clearingAccount = ''
        this.clearingIntent = ''
        this.algoStrategy = ''
        this.algoParams = []   //List[TagValue] = field(default_factory=list)
        this.smartComboRoutingParams = []  //List[TagValue] = field(default_factory=list)
        this.algoId = ''
        this.whatIf  = false
        this.notHeld  = false
        this.solicited  = false
        this.modelCode = ''
        this.orderComboLegs = []  //List['OrderComboLeg'] = field(default_factory=list)
        this.orderMiscOptions = []   //List[TagValue] = field(default_factory=list)
        this.referenceContractId = 0
        this.peggedChangeAmount = 0.0
        this.isPeggedChangeAmountDecrease  = false
        this.referenceChangeAmount = 0.0
        this.referenceExchangeId = ''
        this.adjustedOrderType = ''
        this.triggerPrice = UNSET_DOUBLE
        this.adjustedStopPrice = UNSET_DOUBLE
        this.adjustedStopLimitPrice = UNSET_DOUBLE
        this.adjustedTrailingAmount = UNSET_DOUBLE
        this.adjustableTrailingUnit = 0
        this.lmtPriceOffset = UNSET_DOUBLE
        this.conditions = [] // List['OrderCondition'] = field(default_factory=list)
        this.conditionsCancelOrder  = false
        this.conditionsIgnoreRth  = false
        this.extOperator = ''
        this.softDollarTier = new SoftDollarTier()   //SoftDollarTier = field(default_factory=SoftDollarTier)
        this.cashQty = UNSET_DOUBLE
        this.mifid2DecisionMaker = ''
        this.mifid2DecisionAlgo = ''
        this.mifid2ExecutionTrader = ''
        this.mifid2ExecutionAlgo = ''
        this.dontUseAutoPriceForHedge  = false
        this.isOmsContainer  = false
        this.discretionaryUpToLimitPrice  = false
        this.autoCancelDate = ''
        this.filledQuantity = UNSET_DOUBLE
        this.refFuturesConId = 0
        this.autoCancelParent  = false
        this.shareholder = ''
        this.imbalanceOnly  = false
        this.routeMarketableToBbo  = false
        this.parentPermId = 0
        this.usePriceMgmtAlgo = false
    }
}


class OrderStatus {
    constructor() {
        this.orderId = 0
        this.status = ''
        this.filled = 0
        this.remaining = 0
        this.avgFillPrice = 0.0
        this.permId = 0
        this.parentId = 0
        this.lastFillPrice = 0.0
        this.clientId = 0
        this.whyHeld = ''
        this.mktCapPrice = 0.0

        // PendingSubmit: ClassVar = 'PendingSubmit'
        // PendingCancel: ClassVar = 'PendingCancel'
        // PreSubmitted: ClassVar = 'PreSubmitted'
        // Submitted: ClassVar = 'Submitted'
        // ApiPending: ClassVar = 'ApiPending'
        // ApiCancelled: ClassVar = 'ApiCancelled'
        // Cancelled: ClassVar = 'Cancelled'
        // Filled: ClassVar = 'Filled'
        // Inactive: ClassVar = 'Inactive'

        // DoneStates: ClassVar = {'Filled', 'Cancelled', 'ApiCancelled'}
        // ActiveStates: ClassVar = {
        //     'PendingSubmit', 'ApiPending', 'PreSubmitted', 'Submitted'}
    }
}

class OrderState {
    constructor(){
        this.status = ''
        this.initMarginBefore = ''
        this.maintMarginBefore = ''
        this.equityWithLoanBefore = ''
        this.initMarginChange = ''
        this.maintMarginChange = ''
        this.equityWithLoanChange = ''
        this.initMarginAfter = ''
        this.maintMarginAfter = ''
        this.equityWithLoanAfter = ''
        this.commission = UNSET_DOUBLE
        this.minCommission  = UNSET_DOUBLE
        this.maxCommission  = UNSET_DOUBLE
        this.commissionCurrency = ''
        this.warningText = ''
        this.completedTime = ''
        this.completedStatus = ''
    }
}

class Contract {
    constructor() {
        this.secType = ''
        this.conId = 0
        this.symbol = ''
        this.lastTradeDateOrContractMonth = ''
        this.strike = 0.0
        this.right = ''
        this.multiplier = ''
        this.exchange = ''
        this.primaryExchange = ''
        this.currency = ''
        this.localSymbol = ''
        this.tradingClass = ''
        this.includeExpired = false
        this.secIdType = ''
        this.secId = ''
        this.comboLegsDescrip = ''
        this.comboLegs = [] //List['ComboLeg'] = field(default_factory=list)
        this.deltaNeutralContract = null //Optional['DeltaNeutralContract'] = None
    }
}

class Fill {
    constructor() {
        this.contract = new Contract()
        this.execution = new Execution()
        this.commissionReport = new CommissionReport()
        this.time =  Date()
    }
}

class Execution {
    constructor() {
        this.execId = ''
        this.time = new Date() // datetime = field(default=EPOCH)
        this.acctNumber = ''
        this.exchange = ''
        this.side = ''
        this.shares = 0.0
        this.price = 0.0
        this.permId = 0
        this.clientId = 0
        this.orderId = 0
        this.liquidation = 0
        this.cumQty = 0.0
        this.avgPrice = 0.0
        this.orderRef = ''
        this.evRule = ''
        this.evMultiplier = 0.0
        this.modelCode = ''
        this.lastLiquidity = 0
    }
}

class CommissionReport {
    constructor() {
        this.execId = ''
        this.commission = 0.0
        this.currency = ''
        this.realizedPNL = 0.0
        this.yield_ = 0.0
        this.yieldRedemptionDate = 0
    }
}

class TagValue {
    constructor() {
        this.tag = ''
        this.value = ''
    }
}

class TradeLogEntry {
    constructor() {
        this.time = new Date()
        this.status = ''
        this.message = ''
    }
}

class OrderComboLeg {
    constructor() {
        this.price = UNSET_DOUBLE
    }
}

class SoftDollarTier{
    constructor() {
        this.name = ''
        this.val = ''
        this.displayName = ''
    }
}

class DeltaNeutralContract {
    constructor() {
        this.conId = 0
        this.delta = 0.0
        this.price = 0.0
    }
}

class Trade {
    constructor() {
        this.contract = new Contract()
        this.order = new Order()
        this.orderStatus = new OrderStatus()
        this.fills = []  //List[Fill] = field(default_factory=list)
        // this.log = []  //List[TradeLogEntry] = field(default_factory=list)
    }
}

class Bar{
    constructor() {
        this.time = new Date() //Optional[datetime]
        this.open = NaN
        this.high = NaN
        this.low = NaN
        this.close = NaN
        this.volume = 0
        this.count = 0
    }
}
    




export {Order, Contract,OrderStatus, Trade, Bar, OrderState, Fill, TagValue, TradeLogEntry, OrderComboLeg, SoftDollarTier, DeltaNeutralContract}