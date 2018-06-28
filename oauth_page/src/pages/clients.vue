<template>
  <section>
    <a-breadcrumb>
      <a-breadcrumb-item href="">
        <a-icon type="home" />
      </a-breadcrumb-item>
      <a-breadcrumb-item href="">
        <span>{{title}}</span>
      </a-breadcrumb-item>
    </a-breadcrumb>
    <div style="margin-top: 20px">
      <a-button type="danger" @click="add_status = false">客户端管理</a-button>
      <a-button type="primary" @click="add_status = true">添加客户端</a-button>
    </div>
    <div id="clientList" v-if="add_status === false">
      <a-table bordered :dataSource="dataSource" :columns="columns" :pagination="false">
        <template slot="operation" slot-scope="text, record">
          <a-popconfirm
            v-if="dataSource.length"
            title="Sure to delete?"
            @confirm="() => onDelete(record.id)">
            <a href="#">Delete</a>
          </a-popconfirm>
        </template>
      </a-table>
    </div>
    <div id="clientAdd" v-if="add_status === true">
      <a-form layout="horizontal">
        <a-form-item label="客户端名" :required="true" :labelCol="labelCol" :wrapperCol="wrapperCol" >
          <a-input placeholder="请输入客户端名" type="text" v-model="form.client_name">
            <a-icon type="database" slot="prefix"/>
          </a-input>
        </a-form-item>
        <a-form-item label="请求范围"  :required="true" :labelCol="labelCol" :wrapperCol="wrapperCol">
          <a-input placeholder="请输入请求范围" type="text" v-model="form.client_scope">
            <a-icon type="api" slot="prefix" />
          </a-input>
        </a-form-item>
        <a-form-item label="回调地址" :required="true" :labelCol="labelCol" :wrapperCol="wrapperCol">
          <a-input placeholder="请输入Redirect URIs" type="text" v-model="form.redirect_uri">
            <a-icon slot="prefix" type="global"/>
          </a-input>
        </a-form-item>
        <a-form-item label="认证方式"  :required="true" :labelCol="labelCol" :wrapperCol="wrapperCol">
          <a-select defaultValue="authorization_code" @change="handleChange">
            <a-select-option value="authorization_code">授权码模式</a-select-option>
            <a-select-option value="implicit">简化模式</a-select-option>
            <a-select-option value="password">密码模式</a-select-option>
            <a-select-option value="client_credentials">客户端模式</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="返回类型" :required="true" :labelCol="labelCol" :wrapperCol="wrapperCol">
          <a-select defaultValue="code" @change="handleChangeResponse">
            <a-select-option value="code">验证码</a-select-option>
            <a-select-option value="other">其他模式</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item style="text-align: center">
          <a-button type="primary" @click="AddClient">提交信息</a-button>
        </a-form-item>
      </a-form>
    </div>
  </section>
</template>

<script>
import { ApiReq } from '../api'

export default {
  name: 'Clients',
  data () {
    return {
      title: '客户端管理',
      add_status: false,
      form: {
        client_name: '',
        client_scope: '',
        redirect_uri: '',
        grant_type: 'authorization_code',
        response_type: 'code'
      },
      labelCol: { span: 6 },
      wrapperCol: { span: 14 },
      columns: [{
        title: '客户端',
        dataIndex: 'client_name'
      }, {
        title: '客户端ID',
        dataIndex: 'client_id'
      }, {
        title: '客户端密钥',
        dataIndex: 'client_secret'
      }, {
        title: '回调地址',
        dataIndex: 'redirect_uri'
      }, {
        title: '操作',
        dataIndex: 'operation',
        scopedSlots: { customRender: 'operation' }
      }],
      dataSource: []
    }
  },
  methods: {
    handleChange (value) {
      this.form['grant_type'] = value
    },
    handleChangeResponse (value) {
      this.form['response_type'] = value
    },
    async AddClient () {
      if (
        this.form.client_name === '' ||
        this.form.client_scope === '' ||
        this.form.redirect_uri === ''
      ) {
        this.$message.error('请补全相关信息')
      } else {
        let res = await ApiReq(this, '/api/create_client', this.form, true)
        if (res.code === 0) {
          this.$notification.success({
            message: '成功',
            description: res.msg
          })
          this.add_status = true
          await this.get_refresh()
        }
      }
    },
    async get_refresh () {
      let res = await ApiReq(this, '/api/client_info')
      this.dataSource = res.data
    },
    async onDelete (key) {
      let ClientId = key
      let res = await ApiReq(this, '/api/del_client', {client_id: ClientId})
      if (res.code === 0) {
        await this.$notification.success({
          message: '成功',
          description: res.msg
        })
        await this.get_refresh()
      }
    }
  },
  async mounted () {
    await this.get_refresh()
  }
}
</script>

<style scoped>
#clientList {
  min-height: 230px;
  margin-top: 20px;
}
#clientAdd {
  min-height: 230px;
  margin-top: 30px;
}
</style>
