#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64.hpp"
#include <random>
#include <chrono>
#include <cmath>

class SensorNode : public rclcpp::Node {
public:
    SensorNode()
        : Node("sensor_node"),
          gen_(rd_()),
          dist_(0.0, 1.0),
          t_(0.0)
    {
        // パラメータ
        this->declare_parameter("noise_stddev", 0.5);
        this->get_parameter("noise_stddev", noise_stddev_);

        pub_ = this->create_publisher<std_msgs::msg::Float64>("/sensor/raw", 10);

        // タイマー（100ms周期）
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(100),
            std::bind(&SensorNode::publish_data, this)
        );

        // 初期時刻
        prev_time_ = this->now();

        RCLCPP_INFO(this->get_logger(), "Sensor node started (noise=%.2f)", noise_stddev_);
    }

private:
    void publish_data() {
        // ===== dt計算（ここが改善ポイント）=====
        auto now = this->now();
        double dt = (now - prev_time_).seconds();
        prev_time_ = now;

        // 異常dt対策（初回やスリープ復帰など）
        if (dt <= 0.0 || dt > 1.0) {
            dt = 0.1;
        }

        // ===== 時間更新 =====
        t_ += dt;

        // ===== 信号生成 =====
        double signal = std::sin(t_);

        // ===== ノイズ生成 =====
        double noise = dist_(gen_) * noise_stddev_;

        // ===== 合成 =====
        double data = signal + noise;

        std_msgs::msg::Float64 msg;
        msg.data = data;
        pub_->publish(msg);
    }

    // 時間管理
    rclcpp::Time prev_time_;
    double t_;

    // ノイズ
    std::random_device rd_;
    std::mt19937 gen_;
    std::normal_distribution<> dist_;
    double noise_stddev_;

    // ROS
    rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr pub_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<SensorNode>());
    rclcpp::shutdown();
    return 0;
}