<template>
  <section>
    <div class="hreaders">
      <a-breadcrumb>
        <a-breadcrumb-item href="">
          <a-icon type="home" />
        </a-breadcrumb-item>
        <a-breadcrumb-item href="">
          <span>{{title}}</span>
        </a-breadcrumb-item>
      </a-breadcrumb>
    </div>
    <div id="container">
      <div class="operation" style="margin-top: 20px">
        <a-button type="danger">设备管理</a-button>
        <a-button type="primary" @click="visible = true">添加设备</a-button>
      </div>
      <div id="clientList"  style="margin-top: 20px">
      <a-row type="flex" style="float: left;margin-left: 20px" v-for="item in devicesList" :key="item.key">
      <a-col :span="6" :order="4">
        <a-card
        hoverable
        style="width:140px;"
        :bodyStyle="{padding: '0px'}"
        >
        <span class="zones">{{item.zone}}</span>
        <img
        :src="item.icon"
        slot="cover"
        />
        <ul class="ant-card-actions" slot="actions">
          <li style="width: 66.666%;">{{item.deviceName}}</li>
          <li style="width: 33.333%;">
            <a-popconfirm placement="topRight" okText="删除" cancelText="返回" @confirm="del_item(item)">
              <template slot="title">
                <p>{{item.deviceName}}</p>
                <p>{{item.jsonData}}</p>
              </template>
              <a href="#"><a-icon type="folder-open" /></a>
            </a-popconfirm>
          </li>
        </ul>
      </a-card>
      </a-col>
      </a-row>
      </div>
    </div>
    <div>
      <a-modal
        title="添加设备"
        v-model="visible"
        :footer="null"
        align="center"
      >
      <div style="margin: auto;text-align: center">
        <span><a-icon type="info-circle-o" style="color: #46a6ff"/>根据您的需要选择添加设备类型</span><br><br>
        <a-button type="primary" icon="rocket" size="large" @click="add_entity_device" style="margin-right: 20px">添加真实设备</a-button>
        <a-button type="danger" icon="bulb"  size="large" @click="add_virtual_device">添加虚拟设备</a-button>
      </div>
      </a-modal>
    </div>
  </section>
</template>

<script>
import {ApiReq} from '../api'

export default {
  name: 'Devices',
  data () {
    return {
      title: '设备管理',
      visible: false,
      detail: false,
      devicesList: [],
      deviceTypeData: [{'title': '电视', 'value': 'television'}, {'title': '灯', 'value': 'light'}, {'title': '空调', 'value': 'aircondition'}, {'title': '空气净化器', 'value': 'airpurifier'}, {'title': '插座', 'value': 'outlet'}, {'title': '开关', 'value': 'switch'}, {'title': '扫地机器人', 'value': 'roboticvacuum'}, {'title': '窗帘', 'value': 'curtain'}, {'title': '加湿器', 'value': 'humidifier'}, {'title': '风扇', 'value': 'fan'}, {'title': '暖奶器', 'value': 'bottlewarmer'}, {'title': '豆浆机', 'value': 'soymilkmaker'}, {'title': '电热水壶', 'value': 'kettle'}, {'title': '饮水机', 'value': 'watercooler'}, {'title': '电饭煲', 'value': 'cooker'}, {'title': '热水器', 'value': 'waterheater'}, {'title': '烤箱', 'value': 'oven'}, {'title': '净水器', 'value': 'waterpurifier'}, {'title': '冰箱', 'value': 'fridge'}, {'title': '机顶盒', 'value': 'STB'}, {'title': '传感器', 'value': 'sensor'}, {'title': '洗衣机', 'value': 'washmachine'}, {'title': '智能床', 'value': 'smartbed'}, {'title': '香薰机', 'value': 'aromamachine'}, {'title': '窗', 'value': 'window'}],
      actionsData: [{'title': '打开', 'value': 'TurnOn'}, {'title': '关闭', 'value': 'TurnOff'}, {'title': '频道切换', 'value': 'SelectChannel'}, {'title': '频道增加', 'value': 'AdjustUpChannel'}, {'title': '频道减少', 'value': 'AdjustDownChannel'}, {'title': '声音按照步长调大', 'value': 'AdjustUpVolume'}, {'title': '声音按照步长调小', 'value': 'AdjustDownVolume'}, {'title': '声音调到某个值', 'value': 'SetVolume'}, {'title': '设置静音', 'value': 'SetMute'}, {'title': '取消静音', 'value': 'CancelMute'}, {'title': '播放', 'value': 'Play'}, {'title': '暂停', 'value': 'Pause'}, {'title': '继续', 'value': 'Continue'}, {'title': '下一首或下一台', 'value': 'Next'}, {'title': '上一首或下一台', 'value': 'Previous'}, {'title': '设置亮度', 'value': 'SetBrightness'}, {'title': '调大亮度', 'value': 'AdjustUpBrightness'}, {'title': '调小亮度', 'value': 'AdjustDownBrightness'}, {'title': '设置温度', 'value': 'SetTemperature'}, {'title': '调高温度', 'value': 'AdjustUpTemperature'}, {'title': '调低温度', 'value': 'AdjustDownTemperature'}, {'title': '设置风速', 'value': 'SetWindSpeed'}, {'title': '调大风速', 'value': 'AdjustUpWindSpeed'}, {'title': '调小风速', 'value': 'AdjustDownWindSpeed'}, {'title': '模式的切换', 'value': 'SetMode'}, {'title': '设置颜色', 'value': 'SetColor'}, {'title': '打开功能', 'value': 'OpenFunction'}, {'title': '关闭功能', 'value': 'CloseFunction'}, {'title': '查询颜色', 'value': 'QueryColor'}, {'title': '查询电源开关', 'value': 'QueryPowerState'}, {'title': '查询温度', 'value': 'QueryTemperature'}, {'title': '查询湿度', 'value': 'QueryHumidity'}, {'title': '查询风速', 'value': 'QueryWindSpeed'}, {'title': '查询亮度', 'value': 'QueryBrightness'}, {'title': '查询雾量', 'value': 'QueryFog'}, {'title': '查询模式', 'value': 'QueryMode'}, {'title': '查询pm2.5含量', 'value': 'QueryPM25'}, {'title': '查询方向', 'value': 'QueryDirection'}, {'title': '查询角度', 'value': 'QueryAngle'}],
      propertiesData: [{'title': 'powerstate', 'name': '电源状态', 'value': 'off'}, {'title': 'color', 'name': '颜色', 'value': 'Red'}, {'title': 'temperature', 'name': '温度', 'value': '1'}, {'title': 'windspeed', 'name': '风速', 'value': '1'}, {'title': 'brightness', 'name': '亮度', 'value': '1'}, {'title': 'fog', 'name': '雾量', 'value': '1'}, {'title': 'humidity', 'name': '湿度', 'value': '1'}, {'title': 'pm2.5', 'name': 'pm2.5', 'value': '1'}, {'title': 'channel', 'name': '电视频道', 'value': '东方卫视'}, {'title': 'number', 'name': '电视频道号', 'value': '1'}, {'title': 'direction', 'name': '方向', 'value': 'left'}, {'title': 'angle', 'name': '角度', 'value': '1'}, {'title': 'anion', 'name': '负离子功能', 'value': 'off'}, {'title': 'effluent', 'name': '出水功能', 'value': 'off'}, {'title': 'mode', 'name': '模式', 'value': '参考mode auto'}, {'title': 'lefttime', 'name': '剩余时间', 'value': '1'}, {'title': 'remotestatus', 'name': '设备远程状态', 'value': 'off'}]
    }
  },
  methods: {
    add_virtual_device () {
      this.visible = false
      this.$router.replace('addVirtual')
    },
    add_entity_device () {
      this.visible = false
      this.$router.replace('add')
    },
    async del_item (item) {
      let did = item.id
      let res = await ApiReq(this, '/api/del_devices', {d_id: did})
      if (res.code === 0) {
        await this.$notification.success({
          message: '成功',
          description: res.msg
        })
        await this.get_devices()
      }
    },
    async get_devices () {
      let res = await ApiReq(this, '/api/get_devices_list')
      if (res.code === 0) {
        this.devicesList = res.data
      }
    }
  },
  async mounted () {
    await this.get_devices()
  }
}
</script>

<style scoped>
.zones {
  background-color: #2bc861;
  border-radius: 2px;
  top: 0;
  color: #fff;
  font-size: 14px;
  height: 20px;
  line-height: 20px;
  position: absolute;
  right: 10px;
  text-align: center;
  width: 40px;
}
</style>
