<template>
  <section>
    <a-card
      hoverable
      style="width: 360px;margin: auto"
    >
      <img
        alt="example"
        src="../../static/images/logo.png"
        slot="cover"
      />
      <ul class="ant-card-actions" slot="actions">
        <li style="width: 33.3333%;"><a-button type="primary" @click="confirmAuth"><a-icon type="setting" />同意授权</a-button></li>
        <li style="width: 33.3333%;"><a-button type="danger"><a-icon type="edit" />取消授权</a-button></li>
        <li style="width: 33.3333%;"><a-button><a-icon type="ellipsis" />跳转主页</a-button></li>
      </ul>
      <a-card-meta
        :title="name"
        :description="'正在获取' +scope_deal + '权限'">
      </a-card-meta>
    </a-card>
  </section>
</template>

<script>
import {ApiReq} from '../api'

export default {
  name: 'Authorize',
  data () {
    return {
      name: '',
      redirect_uri: '',
      scope: '',
      uri: ''
    }
  },
  methods: {
    async confirmAuth () {
      let res = await ApiReq(this,
        '/oauth/authorize_confirm',
        {redirect_uri: this.redirect_uri, name: this.name})
      console.log(res)
      if (res.code === 0) {
        this.$notification.success({
          message: '成功',
          description: '验证成功'
        })
        this.uri = res.url
        window.location.replace(this.uri)
      }
    }
  },
  mounted () {
    let params = this.$route.params
    this.name = params.name
    this.redirect_uri = params.redirect_uri
    this.scope = params.scope
  },
  computed: {
    scope_deal () {
      if (this.scope === 'profile') {
        return '个人信息'
      } else if (this.scope === 'devices') {
        return '设备信息'
      }
    }
  },
  created () {
    window.localStorage.setItem('path', this.$route.fullPath)
    if (window.localStorage.getItem('username') && window.localStorage.getItem('sid')) {
      console.log('welcome')
    } else {
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>

</style>
