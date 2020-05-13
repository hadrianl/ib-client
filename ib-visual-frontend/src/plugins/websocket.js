import EventEmitter from "eventemitter3"
import Vue from 'vue'


class IBWebsocket extends EventEmitter {
    constructor (url, options = {}) {
        super()
        this.url = url
        this.ws = null
        this.queue = []

        this.reconnect = true
        this.reconnectTask = null
        this.reconnectInterval = options.reconnectInterval ? options.reconnectInterval : 3000
        this.reconnectMaxTimes = options.reconnectMaxTimes ? options.reconnectMaxTimes : 2
        this.WebSocket = options.WebSocket ? options.WebSocket : WebSocket
        this.reconnectTimes = 0

    }
    
    send (obj) {
        const objToJson = JSON.stringify(obj)
        if (this.isReady()) {
          this.ws.send(objToJson)
        } else {
          this.queue.push(objToJson)
        }
      }

    setUrl (hostname) {
      this.url = `ws://${hostname}:6789`
    }

    isReady () {
      return this.ws && this.ws.readyState === this.WebSocket.OPEN
    }

    init (isReconnection = true) {
      this.ws = new this.WebSocket(this.url)
  
      if (isReconnection) this.reconnectTimes += 1
   
      this.ws.onmessage = (message) => {
        const msg = JSON.parse(message.data)
        this.emit(msg.t, msg.data)
      }

      this.ws.onclose = (event) => {
          this.emit('close')
          this.queue.splice(0, this.queue.length)

          if (event.code === 1001) this.reconnect = false
          // if not reconnect , then return
          if (!this.reconnect) return

          if (this.reconnectMaxTimes <= this.reconnectTimes) {
            clearTimeout(this.reconnectTask)
            this.emit('death', {msg: '超过重连次数' + this.reconnectMaxTimes})
          } else {
            this.reconnectTask = setTimeout(
              () => {
                if (this.ws.readyState === this.WebSocket.CLOSED) {
                  this.init(true)
                  this.emit('reconnect', {msg: '发起重连第 ' + this.reconnectTimes + ' 次'})
                }
              }, 
              this.reconnectInterval)
          }
          
        }

      this.ws.onerror = (error) => {
          this.emit('error', error)
          this.ws.close()
        }

      this.ws.onopen = () => {
          this.emit('open', {msg: '发起重连第 ' + this.reconnectTimes + ' 次, 成功'})
          if (this.reconnectTask) {
            clearTimeout(this.reconnectTask)
          }
          while (this.queue.length > 0) {
            if (this.ws.readyState !== 1) break
            this.ws.send(this.queue.shift())
          }
        }
      }

    close () {
            this.ws.onclose = () => {}
            this.ws.close()
          }

}

const ibws = new IBWebsocket('ws://localhost:6789')
Vue.$ibws = Vue.prototype.$ibws = Vue.$ibws || ibws

export default ibws;