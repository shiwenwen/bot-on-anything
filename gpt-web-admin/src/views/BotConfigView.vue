<template>
  <el-form ref="form" :model="config" label-width="100px">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>通道选择</span>
        </div>
      </template>
      <el-form-item label="通道类型">
        <el-select v-model="config.channel.type" placeholder="请选择">
          <el-option label="微信" value="wechat"></el-option>
        </el-select>
      </el-form-item>
      <el-card class="box-card">
      <template #header>
          <div class="card-header">
            <span>微信</span>
          </div>
          <el-tooltip
            content="只有通过该前缀聊天的单聊对话才会触发AI，避免单聊时对所有接收到的消息进行响应，配置多个请使用英文“,”号分割，若不配置，则默认所有对话都会进行回复。"
          >
            <el-form-item label="单聊触发前缀">
              <el-input v-model="config.channel.wechat.single_chat_prefix" placeholder="配置多个请使用英文“,”号分割"/>
            </el-form-item>
          </el-tooltip>
          <el-tooltip
            content="单聊回复前缀，用于区分是否为AI回复"
          >
            <el-form-item label="单聊回复前缀">
              <el-input v-model="config.channel.wechat.single_chat_reply_prefix" placeholder="单聊回复前缀，用于区分是否为AI回复"/>
            </el-form-item>
          </el-tooltip>
          <el-tooltip
            content="群聊白名单，只有在白名单内的群里支持使用AI助手，多个群名用英文“,”号分割，如开放所有群，请输入ALL_GROUP"
          >
            <el-form-item label="群聊白名单">
              <el-input v-model="config.channel.wechat.group_name_white_list" placeholder="群聊白名单，只有在白名单内的群里支持使用AI助手，多个群名用英文“,”号分割，如开放所有群，请输入ALL_GROUP"/>
            </el-form-item>
          </el-tooltip>
        </template>
      </el-card>
    </el-card>
  </el-form>
</template>

<script lang="ts">
export default {
  data() {
    return {
      config: {
        channel: {
          type: 'wechat',
          wechat: {
            single_chat_prefix: 'BOT', // 多个
            single_chat_reply_prefix: '[🤖]',
            group_name_white_list: '', // 多个
          }
        }
      }
    }
  },
  methods: {
    onSubmit() {
      console.log('submit!')
    }
  }
}
</script>

<style>
</style>
