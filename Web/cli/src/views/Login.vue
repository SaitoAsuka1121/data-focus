<template>
	<div class="root">
		<div>
			<div class="bgimg"></div>
			<div class="bgimg2"></div>
		</div>
		<div class="mainbox">
			<div class="left"></div>
			<div class="right">
				<div class="box" v-show="type == 'login'">
					<el-form
						class="el-form"
						:model="from"
						:inline="false"
						:rules="rules"
						title="登录"
						ref="form"
					>
						<el-form-item prop="username">
							<el-input
								class="el-input"
								v-model="from.username"
								placeholder="Username"
								clearable
								prefix-icon="el-icon-user-solid"
							>
							</el-input>
							<!-- 用户账号输入 -->
						</el-form-item>
						<el-form-item prop="password">
							<el-input
								class="el-input"
								v-model="from.password"
								placeholder="Password"
								show-password
								prefix-icon="el-icon-lock"
							>
							</el-input>
							<!-- 用户密码输入 -->
						</el-form-item>
						<div class="resButton">
							<el-button
								style="width: 75px;"
								@click="type = 'register'"
								type="text"
							>
								注册
							</el-button>
						</div>
						<div class="loginButton">
							<el-button
								style="width: 170px;"
								@click="onSubmit('form')"
								round
								type="primary"
							>
								登录
							</el-button>
						</div>
						<!-- 登录按钮 -->
					</el-form>
				</div>
				<div class="resbox" v-show="type == 'register'">
					<register />
					<div class="resButton">
						<el-button
							style="width: 75px;position: relative;left:13px;top:-70px;"
							@click="type = 'login'"
							type="text"
						>
							已有账号?
						</el-button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
<script>
import Register from './Register.vue';
export default {
	name: 'Login',
	components: { Register },
	data() {
		return {
			type: 'login',
			from: {
				username: '',
				password: ''
			},
			rules: {
				username: [
					{ required: true, message: '请输入账号', trigger: 'blur' },
					{
						min: 1,
						max: 12,
						message: '账号长度应在5到12个字符之间',
						trigger: 'blur'
					}
				],
				password: [
					{ required: true, message: '请输入密码', trigger: 'blur' },
					{
						min: 1,
						max: 12,
						message: '密码长度应在5到12个字符之间',
						trigger: 'blur'
					}
				]
			}
		};
	},
	methods: {
		onSubmit(form) {
			this.$refs[form].validate(valid => {
				if (valid) {
					let { username, password } = this.from;
					let data = { username: username, password: password };
					this.$axios.post('/auth/login', data).then(res => {
						console.log(res);
						if (res.data.code == 0) {
							sessionStorage.setItem('username', username);
							this.$router.push('/database');
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

<style lang="less" scoped >
.bgimg2 {
	background: url(../../images/lbx.png);
	height: 100%;
	width: 100%;
	position: fixed;
	left: 75rem;
	top: -17rem;
	background-repeat: no-repeat;
	overflow: auto;
	opacity: 0.2;
}
@keyframes rotate1 {
	form {
		transform: translate(-50%, -50%) rotate(0deg);
	}
	to {
		transform: translate(-50%, -50%) rotate(360deg);
	}
}
.bgimg {
	background: url(../../images/lbx.png);
	height: 100%;
	width: 100%;
	position: fixed;
	left: -12.5rem;
	top: 28.125rem;
	background-repeat: no-repeat;
	overflow: auto;
	opacity: 0.2;
}
.mainbox {
	// background-color: pink;
	width: 43.75rem;
	height: 25rem;
	left: 25rem;
	top: 9.375rem;
	position: absolute;
	box-shadow: 2px 2px 10px #909090;
	background-color: white;
	border-radius: 2%;
	.left {
		// background-color: red;
		width: 28.125rem;
		position: relative;
		height: 25rem;
		border-right: 1px solid rgba(0, 0, 0, 0.2);
		background: url('../../images/屏幕截图 2021-07-07 004333.png') no-repeat;
		background-size: 100% 100%;
		border-radius: 2% 0% 0% 2%;
	}
	.right {
		width: 15.625rem;
		position: relative;
		height: 25rem;
		left: 28.125rem;
		top: -25rem;

		// background-color: black;
		.box {
			position: absolute;
			top: 6.25rem;
			width: 12.5rem;
			left: 1.5625rem;
		}
	}
}

.el-input  /deep/ .el-input__inner {
	height: 32px;
	border: 0;
	border-bottom: 1px solid rgba(0, 0, 0, 0.2);
	border-radius: 0%;
}

.resButton {
	position: relative;
	left: -5rem;
	top: -1rem;
}
.resbox {
	position: absolute;
	top: 5rem;
	width: 12.5rem;
	left: 1.5625rem;
}
</style>
