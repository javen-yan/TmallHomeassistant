/* eslint-disable camelcase */
let _base_url = 'http://127.0.0.1:8000/v1'
if (process && process.env && process.env.NODE_ENV === 'production') {
  _base_url = 'https://oauth.ealine.cn/v1'
}
export const BASE_URL = _base_url

export const ApiReq = async function (obj, apiUrl, params, usePost = false) {
  let sid = window.localStorage.getItem('sid')
  try {
    let res = null
    if (usePost) {
      res = await obj.$http({
        method: 'POST',
        url: BASE_URL + apiUrl,
        headers: {
          'sid': sid
        },
        timeout: 5000,
        data: params
      })
    } else {
      res = await obj.$http.get(BASE_URL + apiUrl, {
        params,
        timeout: 5000,
        headers: {
          'sid': sid
        }
      })
    }
    if (res.data.code === 0) {
      return res.data
    } else {
      obj.$message.error(res.data.msg)
      return res.data
    }
  } catch (e) {
    obj.$message.error(e)
  }
}
