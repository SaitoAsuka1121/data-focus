<template>
	<div class="root">
		<div class="register">
			<el-form
				class="el-form"
				:model="from"
				:inline="false"
				:rules="rules"
				title="注册"
				ref="form"
			>
				<el-form-item prop="userId">
					<el-input
						v-model="from.userId"
						placeholder="用户名"
						clearable
						prefix-icon="el-icon-user-solid"
					>
					</el-input>
					<!-- 用户账号输入 -->
				</el-form-item>

				<el-form-item prop="password">
					<el-input
						v-model="from.password"
						placeholder="密码"
						show-password
						prefix-icon="el-icon-lock"
					>
					</el-input>
					<!-- 用户密码输入 -->
				</el-form-item>
				<el-form-item prop="againpassword">
					<el-input
						v-model="from.againpassword"
						placeholder="请再次输入密码"
						show-password
						prefix-icon="el-icon-lock"
					>
					</el-input>
					<!-- 用户密码输入 -->
				</el-form-item>

				<br /><br />
				<el-button
					style="width: 170px;"
					@click="onSubmit('form')"
					round
					type="primary"
				>
					注册
				</el-button>
				<!-- 注册按钮 -->
			</el-form>
		</div>
	</div>
</template>
<script>
export default {
	name: 'Register',
	components: {},
	data() {
		var validatePass2 = (rule, value, callback) => {
			if (value == '') {
				callback(new Error('请再次输入密码'));
			} else if (value != this.from.password) {
				callback(new Error('两次输入密码不一致'));
			} else {
				callback();
			}
		};
		return {
			from: {
				userId: '',
				password: '',
				againpassword: ''
			},
			rules: {
				userId: [
					{ required: true, message: '请输入账号', trigger: 'blur' },
					{
						min: 1,
						max: 12,
						message: '账号长度应在8到12个字符之间',
						trigger: 'blur'
					}
				],
				password: [
					{ required: true, message: '请输入密码', trigger: 'blur' },
					{
						min: 1,
						max: 12,
						message: '密码长度应在8到12个字符之间',
						trigger: 'blur'
					}
				],
				againpassword: [
					{ required: true, message: '请输入密码', trigger: 'blur' },
					{
						min: 1,
						max: 12,
						message: '密码长度应在8到12个字符之间',
						trigger: 'blur'
					},
					{ required: true, validator: validatePass2, trigger: 'blur' }
				]
			}
		};
	},
	methods: {
		onSubmit(form) {
			this.$refs[form].validate(valid => {
				if (valid) {
					let { userId, password } = this.from;
					let data = { username: userId, password: password };
					this.$axios.post('/auth/register', data).then(res => {
						if (res.data.code == 0) {
							this.$message({
								message: '注册成功',
								type: 'success'
							});
						} else {
							this.$message({
								message: res.data.message,
								type: 'error'
							});
						}
					});
				}
			});
		}
	}
};
</script>
<style lang="less" scoped>
.resButton {
	position: relative;
	left: 30px;
	top: -1rem;
}
/deep/ .el-input__inner {
	height: 32px;
	border: 0;
	border-bottom: 1px solid rgba(0, 0, 0, 0.2);
	border-radius: 0%;
}
</style>
