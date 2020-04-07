import EventEmitter from "eventemitter3"


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

        this.STATUS = {
            CONNECTING: 0,
            OPEN: 1,
            CLOSING: 2,
            CLOSED: 3
          }

          // this.__init(false)
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
  
      if (isReconnection) {
        this.reconnectTimes += 1
      }
  
      const _this = this
  
      this.ws.onmessage = function (message) {
        // eslint-disable-next-line no-eval
        console.log('message', message)
        const msg = JSON.parse(message.data)
        _this.emit(msg.t, msg.data)


        // if ('trade' in data) {
        //   _this.emit('trade', data['trade'])
        // }else if ('trades' in data) {
        //   _this.emit('trades', data['trades'])
        // }else if ('contract' in data){
        //   _this.emit('contract', data['contract'])
        // }else if ('error' in data) {
        //   _this.emit('error', data['error'])
        // }else if ('bars' in data){
        //   _this.emit('bars', data['bars'])
        // }else if ('bar' in data){
        //   _this.emit('bar', data['bar'])
        // }

        // const data = eval('(' + message.data + ')')
        // _this.emit('message', data)
      //   setImmediate(function () {
      //     _this.ws.send('{"aid":"peek_message"}')
      //   })
      }

      this.ws.onclose = function (event) {
          console.log('close', event)
          _this.emit('close')
          // 清空 queue
          _this.queue = []
          // 自动重连
          if (_this.reconnect) {
            if (_this.reconnectMaxTimes <= _this.reconnectTimes) {
              clearTimeout(_this.reconnectTask)
              _this.emit('death', {
                msg: '超过重连次数' + _this.reconnectMaxTimes
              })
            } else {
              _this.reconnectTask = setTimeout(function () {
                if (_this.ws.readyState === 3) {
                  // 每次重连的时候设置 _this.reconnectUrlIndex
                  // _this.reconnectUrlIndex = (_this.reconnectUrlIndex + 1) < _this.urlList.length ? _this.reconnectUrlIndex + 1 : 0
                  _this.init(true)
                  _this.emit('reconnect', {
                    msg: '发起重连第 ' + _this.reconnectTimes + ' 次'
                  })
                }
              }, _this.reconnectInterval)
            }
          }
        }

      this.ws.onerror = error => {
        console.log('error', error)
          _this.emit('error', error)
          _this.ws.close()
        }

      this.ws.onopen = function () {
        console.log('open')
          _this.emit('open', {
            msg: '发起重连第 ' + _this.reconnectTimes + ' 次, 成功'
          })
          if (this.reconnectTask) {
            clearTimeout(_this.reconnectTask)
          }
          while (_this.queue.length > 0) {
            if (_this.ws.readyState === 1) _this.ws.send(_this.queue.shift())
            else break
          }
        }
      }

    close () {
            this.ws.onclose = () => {}
            this.ws.close()
          }

}

export default IBWebsocket;