<template>
  <section>
  <div class="hreaders">
    <a-breadcrumb>
      <a-breadcrumb-item href="">
        <a-icon type="home" />
      </a-breadcrumb-item>
      <a-breadcrumb-item href="">
        <span>添加虚拟设备</span>
      </a-breadcrumb-item>
    </a-breadcrumb>
  </div>
    <div id="add-forms">
      <div style="text-align: center;margin-bottom: 10px;color: #b3b3b3">填写下面的信息，生成配置文件。</div>
      <a-form layout="horizontal">
        <a-form-item label="设备ID" :required="true" :labelCol="labelCol" :wrapperCol="wrapperCol" >
          <!--<a-select  placeholder="请选择您的设备" @change="handleChange">-->
            <!--<a-select-option v-for="item in devices" :key="item">{{item}}</a-select-option>-->
          <!--</a-select>-->
          <a-input placeholder="请输入deviceID" v-model="deviceID" ></a-input>
        </a-form-item>
        <a-form-item label="设备名称" :required="true" :labelCol="labelCol" :wrapperCol="wrapperCol" >
          <a-input placeholder="请输入deviceName" v-model="deviceName" ></a-input>
        </a-form-item>
        <a-form-item label="设备类型" :required="true" :labelCol="labelCol" :wrapperCol="wrapperCol" >
          <a-input placeholder="请选择设备类型" v-model="deviceType" ></a-input>
        </a-form-item>
        <a-form-item label="设备位置" :required="true" :labelCol="labelCol" :wrapperCol="wrapperCol" >
          <a-select  placeholder="请选择设备位置" @change="handleChangeZone">
            <a-select-option v-for="item in zoneData" :key="item">{{item}}</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="设备品牌" :required="true" :labelCol="labelCol" :wrapperCol="wrapperCol" >
          <a-input v-model="brand" ></a-input>
        </a-form-item>
        <a-form-item label="设备型号" :required="true" :labelCol="labelCol" :wrapperCol="wrapperCol" >
          <a-input v-model="models" ></a-input>
        </a-form-item>
        <a-form-item label="设备图标" :required="true" :labelCol="labelCol" :wrapperCol="wrapperCol" >
          <a-input v-model="icon">
            <img :src="icon" slot="addonAfter" style="width: 32px;height: 32px">
          </a-input>
        </a-form-item>
        <a-form-item label="设备支持属性" :required="true" :labelCol="labelCol" :wrapperCol="wrapperCol" >
          <a-select mode="multiple"  placeholder="请选择支持的设备属性" @change="handleChangeProprity">
            <a-select-option v-for="item in propertiesData" :key="item.title+','+item.value">{{item.name}}</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item  label="支持操作类型" :required="true" :labelCol="labelCol" :wrapperCol="wrapperCol" >
          <a-select mode="multiple"  placeholder="请选择支持的操作类型" @change="handleChangeAction">
            <a-select-option v-for="item in actionsData" :key="item.value">{{item.title}}</a-select-option>
          </a-select>
        </a-form-item>
        <div v-for="(itemm, indexx) in states" :key="itemm.index">
          <a-form-item label="设备属性" :required="true" :labelCol="labelCol" :wrapperCol="wrapperCol" >
            <a-select  placeholder="请选择支持的设备属性" @change="handleChangeState">
              <a-select-option v-for="item in statesData" :key="item.title+','+item.value + ','+ indexx">{{item.name}}</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="子设备" :required="true" :labelCol="labelCol" :wrapperCol="wrapperCol" >
            <a-select  placeholder="请选择您的设备" @change="handlesingleChange">
            <a-select-option v-for="item in devices" :key="item+','+ indexx">{{item}}</a-select-option>
            </a-select>
            <a-button icon="delete" @click="delshuxing(indexx)">删除属性</a-button>
          </a-form-item>
        </div>
        <a-form-item style="text-align: center">
          <a-button type="danger" icon="plus-circle-o" @click="AddState">添加属性</a-button>
        </a-form-item>
        <a-form-item style="text-align: center">
          <a-button type="primary"  @click="AddDevices">提交信息</a-button>
        </a-form-item>
      </a-form>
    </div>

  </section>
</template>

<script>
import {ApiReq} from '../api'

export default {
  name: 'addVirtual',
  data () {
    return {
      labelCol: { span: 6 },
      wrapperCol: { span: 14 },
      devices: [],
      deviceID: 'vDevice_',
      deviceName: '传感器',
      deviceType: 'sensor',
      zone: '',
      brand: 'Ealine',
      models: 'EA',
      actions: [],
      properties: [],
      extension: {
        link: 'https://oauth.ealine.cn'
      },
      icon: 'https://home-assistant.io/demo/favicon-192x192.png',
      jsonData: {},
      states: [
        {
          'title': 'temperature',
          'deviceId': ''
        }
      ],
      zoneData: ['门口', '客厅', '卧室', '客房', '主卧', '次卧', '书房', '餐厅', '厨房', '洗手间', '阳台', '宠物房', '老人房', '儿童房', '婴儿房', '浴室', '玄关', '一楼', '二楼', '楼上', '楼下', '影音室', '娱乐室', '工作间', '杂物间', '衣帽间', '保姆房', '花园'],
      deviceTypeData: [{'title': '电视', 'value': 'television'}, {'title': '灯', 'value': 'light'}, {'title': '空调', 'value': 'aircondition'}, {'title': '空气净化器', 'value': 'airpurifier'}, {'title': '插座', 'value': 'outlet'}, {'title': '开关', 'value': 'switch'}, {'title': '扫地机器人', 'value': 'roboticvacuum'}, {'title': '窗帘', 'value': 'curtain'}, {'title': '加湿器', 'value': 'humidifier'}, {'title': '风扇', 'value': 'fan'}, {'title': '暖奶器', 'value': 'bottlewarmer'}, {'title': '豆浆机', 'value': 'soymilkmaker'}, {'title': '电热水壶', 'value': 'kettle'}, {'title': '饮水机', 'value': 'watercooler'}, {'title': '电饭煲', 'value': 'cooker'}, {'title': '热水器', 'value': 'waterheater'}, {'title': '烤箱', 'value': 'oven'}, {'title': '净水器', 'value': 'waterpurifier'}, {'title': '冰箱', 'value': 'fridge'}, {'title': '机顶盒', 'value': 'STB'}, {'title': '传感器', 'value': 'sensor'}, {'title': '洗衣机', 'value': 'washmachine'}, {'title': '智能床', 'value': 'smartbed'}, {'title': '香薰机', 'value': 'aromamachine'}, {'title': '窗', 'value': 'window'}],
      actionsData: [{'title': '打开', 'value': 'TurnOn'}, {'title': '关闭', 'value': 'TurnOff'}, {'title': '频道切换', 'value': 'SelectChannel'}, {'title': '频道增加', 'value': 'AdjustUpChannel'}, {'title': '频道减少', 'value': 'AdjustDownChannel'}, {'title': '声音按照步长调大', 'value': 'AdjustUpVolume'}, {'title': '声音按照步长调小', 'value': 'AdjustDownVolume'}, {'title': '声音调到某个值', 'value': 'SetVolume'}, {'title': '设置静音', 'value': 'SetMute'}, {'title': '取消静音', 'value': 'CancelMute'}, {'title': '播放', 'value': 'Play'}, {'title': '暂停', 'value': 'Pause'}, {'title': '继续', 'value': 'Continue'}, {'title': '下一首或下一台', 'value': 'Next'}, {'title': '上一首或下一台', 'value': 'Previous'}, {'title': '设置亮度', 'value': 'SetBrightness'}, {'title': '调大亮度', 'value': 'AdjustUpBrightness'}, {'title': '调小亮度', 'value': 'AdjustDownBrightness'}, {'title': '设置温度', 'value': 'SetTemperature'}, {'title': '调高温度', 'value': 'AdjustUpTemperature'}, {'title': '调低温度', 'value': 'AdjustDownTemperature'}, {'title': '设置风速', 'value': 'SetWindSpeed'}, {'title': '调大风速', 'value': 'AdjustUpWindSpeed'}, {'title': '调小风速', 'value': 'AdjustDownWindSpeed'}, {'title': '模式的切换', 'value': 'SetMode'}, {'title': '设置颜色', 'value': 'SetColor'}, {'title': '打开功能', 'value': 'OpenFunction'}, {'title': '关闭功能', 'value': 'CloseFunction'}, {'title': '查询颜色', 'value': 'QueryColor'}, {'title': '查询电源开关', 'value': 'QueryPowerState'}, {'title': '查询温度', 'value': 'QueryTemperature'}, {'title': '查询湿度', 'value': 'QueryHumidity'}, {'title': '查询风速', 'value': 'QueryWindSpeed'}, {'title': '查询亮度', 'value': 'QueryBrightness'}, {'title': '查询雾量', 'value': 'QueryFog'}, {'title': '查询模式', 'value': 'QueryMode'}, {'title': '查询pm2.5含量', 'value': 'QueryPM25'}, {'title': '查询方向', 'value': 'QueryDirection'}, {'title': '查询角度', 'value': 'QueryAngle'}],
      propertiesData: [{'title': 'powerstate', 'name': '电源状态', 'value': 'off'}, {'title': 'color', 'name': '颜色', 'value': 'Red'}, {'title': 'temperature', 'name': '温度', 'value': '1'}, {'title': 'windspeed', 'name': '风速', 'value': '1'}, {'title': 'brightness', 'name': '亮度', 'value': '1'}, {'title': 'fog', 'name': '雾量', 'value': '1'}, {'title': 'humidity', 'name': '湿度', 'value': '1'}, {'title': 'pm2.5', 'name': 'pm2.5', 'value': '1'}, {'title': 'channel', 'name': '电视频道', 'value': '东方卫视'}, {'title': 'number', 'name': '电视频道号', 'value': '1'}, {'title': 'direction', 'name': '方向', 'value': 'left'}, {'title': 'angle', 'name': '角度', 'value': '1'}, {'title': 'anion', 'name': '负离子功能', 'value': 'off'}, {'title': 'effluent', 'name': '出水功能', 'value': 'off'}, {'title': 'mode', 'name': '模式', 'value': '参考mode auto'}, {'title': 'lefttime', 'name': '剩余时间', 'value': '1'}, {'title': 'remotestatus', 'name': '设备远程状态', 'value': 'off'}],
      statesData: [{'title': 'powerstate', 'name': '电源状态', 'value': 'on', 'unit': ''}, {'title': 'color', 'name': '颜色', 'value': 'red', 'unit': ''}, {'title': 'temperature', 'name': '温度', 'value': '20', 'unit': '摄氏度'}, {'title': 'windspeed', 'name': '风速', 'value': '1', 'unit': '档'}, {'title': 'brightness', 'name': '亮度', 'value': '20', 'unit': ''}, {'title': 'fog', 'name': '雾量', 'value': '20', 'unit': ''}, {'title': 'humidity', 'name': '湿度', 'value': '20', 'unit': ''}, {'title': 'pm2.5', 'name': 'pm2.5', 'value': '20', 'unit': ''}, {'title': 'channel', 'name': '电视频道', 'value': '山东卫视', 'unit': ''}, {'title': 'number', 'name': '电视频道号', 'value': '20', 'unit': ''}, {'title': 'direction', 'name': '方向', 'value': 'down', 'unit': '无'}, {'title': 'angle', 'name': '角度', 'value': '20', 'unit': '度'}, {'title': 'anion', 'name': '负离子功能', 'value': 'on', 'unit': ''}, {'title': 'effluent', 'name': '出水功能', 'value': 'on', 'unit': ''}, {'title': 'mode', 'name': '模式', 'value': 'mode', 'unit': ''}, {'title': 'lefttime', 'name': '剩余时间', 'value': '20', 'unit': ''}, {'title': 'remotestatus', 'name': '设备远程状态', 'value': 'on', 'unit': ''}]
    }
  },
  methods: {
    handleChange (e) {
      this.deviceID = e
    },
    handlesingleChange (e) {
      let tempstr = e.split(',')
      let index = tempstr[1]
      let deviceid = tempstr[0]
      this.states[index].deviceId = deviceid
    },
    handleChangeZone (e) {
      this.zone = e
    },
    handleChangeAction (e) {
      this.actions = e
    },
    handleChangeProprity (e) {
      let pro = []
      for (let i = 0; i < e.length; i++) {
        let tempstr = e[i].split(',')
        let temp = {'name': tempstr[0], 'value': tempstr[1]}
        pro.push(temp)
      }
      this.properties = pro
    },
    handleChangeState (e) {
      let tempstr = e.split(',')
      let index = tempstr[2]
      let title = tempstr[0]
      this.states[index].title = title
    },
    AddState () {
      const that = this
      let addnew = {
        'title': 'temperature',
        'deviceId': ''
      }
      that.states = that.states.concat(addnew)
    },
    delshuxing (index) {
      const that = this
      that.states.splice(index, 1)
    },
    async AddDevices () {
      this.jsonData = {
        'deviceId': this.deviceID,
        'deviceName': this.deviceName,
        'deviceType': this.deviceType,
        'zone': this.zone,
        'brand': this.brand,
        'model': this.models,
        'icon': this.icon,
        'properties': this.properties,
        'actions': this.actions,
        'extensions': this.extension
      }
      let req = {
        json_data: this.jsonData,
        deviceId: this.deviceID,
        deviceName: this.deviceName,
        zone: this.zone,
        icon: this.icon,
        virtual: 1,
        states: this.states
      }
      let res = await ApiReq(this, '/api/add_devices', req, true)
      if (res && res.code === 0) {
        await this.$notification.success({
          message: '成功',
          description: res.msg
        })
        this.$router.push('/devices')
      }
    },
    async get_init () {
      let res = await ApiReq(this, '/api/get_ha_source')
      if (res && res.code === 0) {
        this.devices = res.data.sensor
      }
    }
  },
  async mounted () {
    await this.get_init()
  }
}
</script>

<style scoped>

</style>
